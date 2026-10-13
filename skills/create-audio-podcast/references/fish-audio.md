# Fish Audio dialogue

Use Fish for synthesis, retaining the shared-discovery writing and source checks. Switching providers sends the spoken script and delivery guidance to Fish; it does not require uploading source documents or publishing the result.

## Setup and first use

1. Have the user create a key at [Fish API Keys](https://fish.audio/app/api-keys). Store it as `FISH_API_KEY` in a protected environment or an owner-readable env file outside version control. Never ask for it in chat.
2. Confirm Drama 3 access and current pricing in the account before a paid call. The [public pricing table](https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits) inspected on October 13, 2026 did not list Drama 3. Do not borrow another model's rate or assume the website's free trial covers this API.
3. Start with a 45–90 second pilot, not the full episode. Request user audition/approval before the first full Fish recording. Preserve the earlier recording for comparison; do not claim improved naturalness from a passing file check.

Use the usual renderer commands with `--provider fish --compress always`. Dry-run reports request count and UTF-8 input bytes including directions. Add `--env-file /absolute/protected/path` for synthesis. No key is needed for dry-run or bundle verification.

## Voices and direction

The starting cast is Delia for Maya and Adrian for Theo, public English voices listed in [Drama 3's documentation](https://docs.fish.audio/features/text-to-speech/drama-3). Their IDs are renderer defaults, not cloned OpenAI voices. Audition them; retain fictional host identities.

Override using host `fish_voice` fields or `--voice-a` / `--voice-b` with Fish voice IDs. OpenAI `voice` names remain separate.

Keep host delivery concise, such as “Warm, curious, conversational; speaking to an equal.” A turn can override it with `"direction": "Thoughtful, gently testing the assumption."` The renderer inserts these cues only in synthesis input. Avoid theatrical reactions. Spoken text and direction fields accept plain text, not inline tags; this prevents source material from inserting speaker-control tokens.

## Contract and limitations

The adapter uses `POST https://api.fish.audio/v1/tts`, an explicit `model: drama-3` header, ordered voice IDs, and speaker markers in one dialogue request. PCM output is requested at 24 kHz, then packaged with the existing WAV/M4A pipeline. See the [API contract](https://docs.fish.audio/api-reference/endpoint/openapi-v1/text-to-speech).

The API documentation warns that unrecognized model names can fall back to another model. The adapter rejects all but `drama-3` and `drama-3-preview`; the manifest records the requested model, not proof of server model identity.

There is no automatic retry or provider fallback: after a timeout, check account usage before retrying. Keep the first paid test short. For long episodes, check for omitted/repeated dialogue and premature endings; technical verification alone does not prove coverage. If necessary, split the script manually at natural scene boundaries, preserve each script, and test continuity rather than switching to isolated sentence calls.

Automated tests mock Fish responses. A successful paid pilot and human audition are required before describing this integration as live-validated.
