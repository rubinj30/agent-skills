# Rendering and recovery

Read this reference when the standard local render cannot produce a verified M4A bundle.

## Mobile packaging preflight

Use `--compress always` for a promised mobile-ready deliverable. It resolves the player template and AAC encoder before the first paid speech request. `--compress auto` may intentionally fall back to WAV, which is useful for archival output but is not a reliable chat or mobile attachment format.

The renderer finds either:

1. `ffmpeg` on `PATH`; or
2. the binary supplied by the optional `imageio-ffmpeg` Python package.

When neither is available, install the optional encoder into a disposable local directory rather than changing the project environment:

```bash
python3 -m pip install --target /tmp/podcast-ffmpeg imageio-ffmpeg
PYTHONPATH=/tmp/podcast-ffmpeg python3 scripts/render_podcast.py podcast-script.json \
  --output-dir podcast-output --compress always
```

Remove the disposable directory after the output bundle passes verification.

## Credential is available only on another machine

Keep the credential on the machine where it already exists. The renderer calls the Speech API with Python's standard library and does not need the OpenAI Python package.

Before transferring a script or source-derived brief to another machine, obtain explicit approval and explain what non-secret content will leave the current workspace. Then:

1. Use a purpose-specific temporary directory.
2. Copy the complete skill directory so `scripts/render_podcast.py` retains access to `assets/mobile-player.html`. If only the script is copied, also copy the template and pass `--template /path/to/mobile-player.html`.
3. Validate credential presence without printing its value.
4. Run the renderer where `OPENAI_API_KEY` is already protected.
5. Copy only the generated deliverables back.
6. Remove the temporary remote files and confirm unrelated services were not restarted or reconfigured.

Do not extract a production credential into command output, logs, shell history, or an artifact. If transfer approval is withheld, keep the validated script and ask the user to provide a protected local API-key path.

## Recover completed synthesis

If a valid WAV exists but compression, player generation, or manifest creation failed, package it without another Speech API call:

```bash
python3 scripts/render_podcast.py podcast-script.json \
  --output-dir podcast-output \
  --output-name episode-name \
  --package-existing podcast-output/episode-name.wav \
  --compress always
```

The recovery path regenerates the transcript, player, and manifest, and preserves the existing lossless audio. Use `--template` if the bundled player asset is not beside the renderer.

## Verify before delivery

Run:

```bash
python3 scripts/render_podcast.py podcast-script.json \
  --output-dir podcast-output \
  --verify-only
```

Verification requires:

- the manifest's audio file to exist and match its SHA-256 hash;
- the manifest's script hash and title to match the current script;
- a positive duration;
- a complete transcript;
- a player that references the current audio file and has no unresolved placeholders; and
- a readable WAV or an M4A with an ISO media header.

Also inspect or listen to the opening, a middle transition, and the ending. Deterministic checks catch packaging defects; they do not judge pronunciation, pacing, or speaker distinction.

For local delivery, attach or link the M4A and offer `index.html` as the richer player. A local HTML path is not proof that another device can access it. For remote delivery, verify the actual URL returns HTTP 200 and the audio endpoint supports byte ranges with HTTP 206.
