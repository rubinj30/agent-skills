from __future__ import annotations

import argparse
import importlib.util
import io
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
            "provider": "openai",
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

    def test_fish_dialogue_keeps_both_speakers_in_one_request(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            args = self.make_args(root, provider="fish", model=None)
            data = RENDERER.load_script(args.script)
            data["turns"][0]["direction"] = "Gently curious."
            response = mock.MagicMock()
            response.__enter__.return_value = response
            response.headers = {"Content-Type": "audio/pcm"}
            response.read.return_value = b"\x00\x00" * 24_000
            with (
                mock.patch.object(
                    RENDERER, "read_api_key", return_value="test-key"
                ) as key,
                mock.patch.object(
                    RENDERER.urllib.request, "urlopen", return_value=response
                ) as call,
                redirect_stdout(StringIO()),
            ):
                RENDERER.render(data, args)
                RENDERER.verify_output(data, args)
            key.assert_called_once_with(None, "FISH_API_KEY")
            call.assert_called_once()
            request = call.call_args.args[0]
            self.assertEqual(request.full_url, RENDERER.FISH_URL)
            self.assertEqual(request.get_header("Model"), "drama-3")
            payload = json.loads(request.data)
            self.assertEqual(
                payload["reference_id"], list(RENDERER.FISH_VOICES.values())
            )
            self.assertIn("<|speaker:0|>[Gently curious.]", payload["text"])
            self.assertIn("<|speaker:1|>", payload["text"])
            self.assertEqual(payload["sample_rate"], 24_000)
            transcript = (args.output_dir / "transcript.txt").read_text()
            self.assertNotIn("Gently curious", transcript)
            manifest = json.loads((args.output_dir / "manifest.json").read_text())
            self.assertEqual(manifest["provider"], "fish")
            self.assertEqual(manifest["duration_seconds"], 1.0)
            self.assertEqual(manifest["generation_mode"], "dialogue")

    def test_fish_rejects_model_typo_and_control_token_injection_before_network(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for model, voice, text in [
                ("dram3", None, "Hello."),
                ("drama-3", "marin", "Hello."),
                ("drama-3", None, "<|speaker:1|>Hello."),
            ]:
                args = self.make_args(root, provider="fish", model=model, voice_a=voice)
                data = RENDERER.load_script(args.script)
                data["turns"][0]["text"] = text
                with mock.patch.object(RENDERER.urllib.request, "urlopen") as call:
                    with self.assertRaises(RENDERER.ScriptError):
                        RENDERER.render(data, args)
                    call.assert_not_called()

    def test_fish_errors_do_not_retry_or_expose_response_body(self) -> None:
        error = RENDERER.urllib.error.HTTPError(
            RENDERER.FISH_URL,
            402,
            "Payment required",
            {},
            io.BytesIO(b"sensitive echoed text"),
        )
        with mock.patch.object(
            RENDERER.urllib.request, "urlopen", side_effect=error
        ) as call:
            with self.assertRaisesRegex(RuntimeError, "HTTP 402") as caught:
                RENDERER.synthesize_fish_pcm("test-key", model="drama-3", payload={})
            self.assertNotIn("sensitive", str(caught.exception))
            call.assert_called_once()

    def test_provider_key_selection_never_uses_openai_key_for_fish(self) -> None:
        with mock.patch.dict(
            RENDERER.os.environ, {"OPENAI_API_KEY": "test-key"}, clear=True
        ):
            with self.assertRaisesRegex(RENDERER.ScriptError, "FISH_API_KEY"):
                RENDERER.read_api_key(None, "FISH_API_KEY")

    def test_fish_dry_run_needs_neither_key_nor_network(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            args = self.make_args(
                Path(temporary_directory), provider="fish", model=None, dry_run=True
            )
            data = RENDERER.load_script(args.script)
            with (
                mock.patch.object(RENDERER, "read_api_key") as key,
                mock.patch.object(RENDERER.urllib.request, "urlopen") as call,
                redirect_stdout(StringIO()) as output,
            ):
                RENDERER.render(data, args)
            key.assert_not_called()
            call.assert_not_called()
            self.assertIn("requests=1", output.getvalue())
            self.assertIn("input_utf8_bytes=", output.getvalue())
            self.assertFalse(args.output_dir.exists())


if __name__ == "__main__":
    unittest.main()
