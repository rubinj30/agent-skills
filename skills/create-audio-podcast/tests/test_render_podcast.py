from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
import unittest
import wave
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_DIR / "scripts" / "render_podcast.py"
SPEC = importlib.util.spec_from_file_location("render_podcast", SCRIPT_PATH)
assert SPEC and SPEC.loader
RENDERER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDERER)


def script_data() -> dict[str, object]:
    return {
        "title": "Test episode",
        "description": "A deterministic renderer test.",
        "source_note": "Generated test fixture.",
        "hosts": {
            "host_a": {
                "name": "Maya",
                "role": "guide",
                "delivery": "Warm and concise.",
                "voice": "marin",
            },
            "host_b": {
                "name": "Theo",
                "role": "analyst",
                "delivery": "Precise and conversational.",
                "voice": "cedar",
            },
        },
        "turns": [
            {"speaker": "host_a", "text": "What are we testing?"},
            {"speaker": "host_b", "text": "Reliable podcast packaging."},
        ],
    }


def write_wav(path: Path) -> None:
    with wave.open(str(path), "wb") as writer:
        writer.setnchannels(1)
        writer.setsampwidth(2)
        writer.setframerate(24_000)
        writer.writeframes(b"\x00\x00" * 24_000)


class RendererTests(unittest.TestCase):
    def make_args(self, root: Path, **overrides: object) -> argparse.Namespace:
        script = root / "podcast-script.json"
        script.write_text(json.dumps(script_data()), encoding="utf-8")
        values: dict[str, object] = {
            "script": script,
            "output_dir": root / "output",
            "output_name": "test-episode",
            "env_file": None,
            "model": RENDERER.DEFAULT_MODEL,
            "voice_a": None,
            "voice_b": None,
            "speed": 1.0,
            "template": None,
            "package_existing": None,
            "compress": "never",
            "dry_run": False,
            "verify_only": False,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_dry_run_does_not_create_output_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            args = self.make_args(root, dry_run=True)
            data = RENDERER.load_script(args.script)
            with redirect_stdout(StringIO()):
                RENDERER.render(data, args)
            self.assertFalse(args.output_dir.exists())

    def test_existing_wav_can_be_packaged_and_verified_without_api(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_wav = root / "source.wav"
            write_wav(source_wav)
            args = self.make_args(root, package_existing=source_wav)
            data = RENDERER.load_script(args.script)

            with redirect_stdout(StringIO()):
                RENDERER.render(data, args)

            self.assertTrue((args.output_dir / "test-episode.wav").is_file())
            self.assertTrue((args.output_dir / "index.html").is_file())
            self.assertTrue((args.output_dir / "manifest.json").is_file())
            self.assertTrue((args.output_dir / "transcript.txt").is_file())

            args.package_existing = None
            args.verify_only = True
            with redirect_stdout(StringIO()):
                RENDERER.render(data, args)

    def test_missing_template_fails_before_api_key_lookup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            args = self.make_args(root, template=root / "missing-template.html")
            data = RENDERER.load_script(args.script)
            with mock.patch.object(RENDERER, "read_api_key") as read_api_key:
                with self.assertRaisesRegex(
                    RuntimeError, "Cannot read mobile-player template"
                ):
                    RENDERER.render(data, args)
            read_api_key.assert_not_called()

    def test_required_compression_fails_before_api_key_lookup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            args = self.make_args(root, compress="always")
            data = RENDERER.load_script(args.script)
            with (
                mock.patch.object(RENDERER, "find_ffmpeg", return_value=None),
                mock.patch.object(RENDERER, "read_api_key") as read_api_key,
            ):
                with self.assertRaisesRegex(RuntimeError, "requires ffmpeg"):
                    RENDERER.render(data, args)
            read_api_key.assert_not_called()


if __name__ == "__main__":
    unittest.main()
