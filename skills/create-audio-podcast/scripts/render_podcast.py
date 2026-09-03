#!/usr/bin/env python3
"""Render a validated two-host podcast script with OpenAI text-to-speech."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SPEECH_URL = "https://api.openai.com/v1/audio/speech"
DEFAULT_MODEL = "gpt-4o-mini-tts"
DEFAULT_VOICES = {"host_a": "marin", "host_b": "cedar"}
SAMPLE_RATE = 24_000
CHANNELS = 1
SAMPLE_WIDTH = 2
MAX_TURN_CHARS = 3_900
RETRYABLE_HTTP_CODES = {408, 409, 429, 500, 502, 503, 504}


class ScriptError(ValueError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a two-host JSON podcast script to audio and a mobile player."
    )
    parser.add_argument("script", type=Path, help="Path to podcast-script.json")
    parser.add_argument("--output-dir", type=Path, default=Path("podcast-output"))
    parser.add_argument("--output-name", default="podcast", help="Safe basename without extension")
    parser.add_argument("--env-file", type=Path, help="Optional env file containing OPENAI_API_KEY")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--voice-a", help="Override host_a voice")
    parser.add_argument("--voice-b", help="Override host_b voice")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument(
        "--compress",
        choices=("auto", "always", "never"),
        default="auto",
        help="Create an AAC M4A with ffmpeg when available",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate without API calls")
    return parser.parse_args()


def require_text(value: Any, label: str, *, max_chars: int | None = None) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ScriptError(f"{label} must be a non-empty string")
    result = value.strip()
    if max_chars is not None and len(result) > max_chars:
        raise ScriptError(f"{label} exceeds {max_chars} characters")
    return result


def load_script(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ScriptError(f"Cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ScriptError("The script root must be a JSON object")

    data["title"] = require_text(data.get("title"), "title", max_chars=180)
    data["description"] = require_text(
        data.get("description"), "description", max_chars=500
    )
    data["source_note"] = require_text(
        data.get("source_note"), "source_note", max_chars=500
    )

    hosts = data.get("hosts")
    if not isinstance(hosts, dict):
        raise ScriptError("hosts must be an object")
    for speaker in DEFAULT_VOICES:
        host = hosts.get(speaker)
        if not isinstance(host, dict):
            raise ScriptError(f"hosts.{speaker} must be an object")
        host["name"] = require_text(host.get("name"), f"hosts.{speaker}.name", max_chars=60)
        host["role"] = require_text(host.get("role"), f"hosts.{speaker}.role", max_chars=180)
        host["delivery"] = require_text(
            host.get("delivery"), f"hosts.{speaker}.delivery", max_chars=500
        )
        voice = host.get("voice", DEFAULT_VOICES[speaker])
        host["voice"] = require_text(voice, f"hosts.{speaker}.voice", max_chars=40)

    turns = data.get("turns")
    if not isinstance(turns, list) or len(turns) < 2:
        raise ScriptError("turns must contain at least two entries")
    seen: set[str] = set()
    for index, turn in enumerate(turns):
        if not isinstance(turn, dict):
            raise ScriptError(f"turns[{index}] must be an object")
        speaker = turn.get("speaker")
        if speaker not in DEFAULT_VOICES:
            raise ScriptError(f"turns[{index}].speaker must be host_a or host_b")
        turn["text"] = require_text(
            turn.get("text"), f"turns[{index}].text", max_chars=MAX_TURN_CHARS
        )
        seen.add(speaker)
    if seen != set(DEFAULT_VOICES):
        raise ScriptError("Both host_a and host_b must speak")
    return data


def read_api_key(env_file: Path | None) -> str:
    value = os.environ.get("OPENAI_API_KEY", "").strip()
    if value:
        return value
    if env_file is None:
        raise ScriptError("Set OPENAI_API_KEY or provide --env-file")
    try:
        lines = env_file.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ScriptError(f"Cannot read env file: {exc}") from exc
    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, separator, candidate = line.partition("=")
        if separator and key.strip() == "OPENAI_API_KEY":
            value = candidate.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    if not value:
        raise ScriptError("OPENAI_API_KEY is empty")
    return value


def speech_instructions(host: dict[str, str]) -> str:
    return (
        f"You are {host['name']}, the {host['role']} in a two-person educational podcast. "
        f"{host['delivery']} Speak only the supplied dialogue. Sound human and spontaneous "
        "while remaining clear. Use subtle changes in pace and emphasis. Avoid an announcer "
        "voice, exaggerated emotion, and added words."
    )


def synthesize_pcm(
    api_key: str,
    *,
    model: str,
    voice: str,
    speed: float,
    instructions: str,
    text: str,
) -> bytes:
    payload = json.dumps(
        {
            "model": model,
            "voice": voice,
            "response_format": "pcm",
            "speed": speed,
            "instructions": instructions,
            "input": text,
        }
    ).encode("utf-8")

    for attempt in range(4):
        request = urllib.request.Request(
            SPEECH_URL,
            data=payload,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                audio = response.read()
            if not audio or len(audio) % (CHANNELS * SAMPLE_WIDTH):
                raise RuntimeError("Speech API returned invalid PCM audio")
            return audio
        except urllib.error.HTTPError as exc:
            details = exc.read(2_000).decode("utf-8", errors="replace")
            if exc.code not in RETRYABLE_HTTP_CODES or attempt == 3:
                raise RuntimeError(f"Speech API returned HTTP {exc.code}: {details}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == 3:
                raise RuntimeError(f"Speech API request failed: {exc}") from exc
        time.sleep(2**attempt)
    raise RuntimeError("Speech API request failed")


def safe_output_name(value: str) -> str:
    if not value or value in {".", ".."} or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for char in value):
        raise ScriptError("--output-name may contain only letters, numbers, hyphens, and underscores")
    return value


def write_transcript(data: dict[str, Any], path: Path) -> None:
    lines = [data["title"], "=" * len(data["title"]), ""]
    for turn in data["turns"]:
        name = data["hosts"][turn["speaker"]]["name"]
        lines.extend((f"{name}:", turn["text"], ""))
    lines.extend((f"Source note: {data['source_note']}", "AI-generated voices."))
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def compress_m4a(wav_path: Path, m4a_path: Path, mode: str) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        if mode == "always":
            raise RuntimeError("--compress always requires ffmpeg")
        return wav_path
    command = [
        ffmpeg,
        "-y",
        "-loglevel",
        "error",
        "-i",
        str(wav_path),
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        str(m4a_path),
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        if mode == "always":
            raise
        return wav_path
    return m4a_path


def duration_label(seconds: float) -> str:
    minutes, remainder = divmod(round(seconds), 60)
    return f"{minutes}:{remainder:02d}"


def write_player(
    data: dict[str, Any], *, audio_path: Path, duration_seconds: float, output_path: Path
) -> None:
    template_path = Path(__file__).resolve().parent.parent / "assets" / "mobile-player.html"
    template = template_path.read_text(encoding="utf-8")
    transcript_parts = []
    for turn in data["turns"]:
        name = html.escape(data["hosts"][turn["speaker"]]["name"])
        spoken = html.escape(turn["text"])
        transcript_parts.append(f"<p><strong>{name}</strong>{spoken}</p>")
    audio_type = "audio/mp4" if audio_path.suffix.lower() == ".m4a" else "audio/wav"
    replacements = {
        "{{TITLE}}": html.escape(data["title"]),
        "{{DESCRIPTION}}": html.escape(data["description"]),
        "{{AUDIO_FILE}}": html.escape(audio_path.name, quote=True),
        "{{AUDIO_TYPE}}": audio_type,
        "{{DURATION}}": duration_label(duration_seconds),
        "{{SOURCE_NOTE}}": html.escape(data["source_note"]),
        "{{TRANSCRIPT}}": "\n".join(transcript_parts),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    output_path.write_text(template, encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def render(data: dict[str, Any], args: argparse.Namespace) -> None:
    output_name = safe_output_name(args.output_name)
    if not 0.25 <= args.speed <= 4.0:
        raise ScriptError("--speed must be between 0.25 and 4.0")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = args.output_dir / "transcript.txt"
    write_transcript(data, transcript_path)

    characters = sum(len(turn["text"]) for turn in data["turns"])
    words = sum(len(turn["text"].split()) for turn in data["turns"])
    estimated_minutes = words / 145
    if args.dry_run:
        print(
            f"valid=true turns={len(data['turns'])} characters={characters} "
            f"estimated_minutes={estimated_minutes:.1f}"
        )
        return

    api_key = read_api_key(args.env_file)
    wav_path = args.output_dir / f"{output_name}.wav"
    partial_path = args.output_dir / f".{output_name}.partial.wav"
    total_frames = 0
    try:
        with wave.open(str(partial_path), "wb") as writer:
            writer.setnchannels(CHANNELS)
            writer.setsampwidth(SAMPLE_WIDTH)
            writer.setframerate(SAMPLE_RATE)
            for index, turn in enumerate(data["turns"], start=1):
                speaker = turn["speaker"]
                host = data["hosts"][speaker]
                voice_override = args.voice_a if speaker == "host_a" else args.voice_b
                voice = voice_override or host["voice"] or DEFAULT_VOICES[speaker]
                pcm = synthesize_pcm(
                    api_key,
                    model=args.model,
                    voice=voice,
                    speed=args.speed,
                    instructions=speech_instructions(host),
                    text=turn["text"],
                )
                writer.writeframesraw(pcm)
                total_frames += len(pcm) // (CHANNELS * SAMPLE_WIDTH)
                if index < len(data["turns"]):
                    pause_frames = round(SAMPLE_RATE * 0.22)
                    writer.writeframesraw(b"\x00" * pause_frames * CHANNELS * SAMPLE_WIDTH)
                    total_frames += pause_frames
                print(f"rendered_turn={index}/{len(data['turns'])} speaker={speaker}")
        partial_path.replace(wav_path)
    except Exception:
        partial_path.unlink(missing_ok=True)
        raise

    duration_seconds = total_frames / SAMPLE_RATE
    audio_path = wav_path
    if args.compress != "never":
        audio_path = compress_m4a(wav_path, args.output_dir / f"{output_name}.m4a", args.compress)
    player_path = args.output_dir / "index.html"
    write_player(data, audio_path=audio_path, duration_seconds=duration_seconds, output_path=player_path)

    manifest = {
        "title": data["title"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "ai_generated_voices": True,
        "model": args.model,
        "voices": {
            "host_a": args.voice_a or data["hosts"]["host_a"]["voice"],
            "host_b": args.voice_b or data["hosts"]["host_b"]["voice"],
        },
        "turns": len(data["turns"]),
        "characters": characters,
        "duration_seconds": round(duration_seconds, 3),
        "audio_file": audio_path.name,
        "audio_sha256": sha256(audio_path),
        "script_sha256": sha256(args.script),
        "source_note": data["source_note"],
    }
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"audio={audio_path}")
    print(f"player={player_path}")
    print(f"duration_seconds={duration_seconds:.1f}")


def main() -> int:
    args = parse_args()
    try:
        data = load_script(args.script)
        render(data, args)
    except (ScriptError, RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
