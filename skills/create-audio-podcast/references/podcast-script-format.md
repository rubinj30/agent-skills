# Podcast script format

## Contents

1. Conversation design
2. Required JSON
3. Spoken-language rules
4. Final review

## Conversation design

Create an original two-host explainer with the energy of a thoughtful studio conversation. Do not imitate named presenters or reproduce another product's wording.

Use this arc:

1. **Cold open:** expose the surprising question, consequence, or tension in under 30 seconds.
2. **Orientation:** tell the listener what will be understood by the end.
3. **Mental model:** explain the core mechanism before details.
4. **Evidence and example:** make the mechanism concrete.
5. **Challenge:** let the guiding host question an assumption, limitation, or failure mode.
6. **Synthesis:** reconcile the answer with the challenge.
7. **Close:** recap the few ideas worth remembering and any practical next step.

Host roles:

- `host_a`: curious facilitator and audience proxy. Frames questions, notices implications, requests concrete examples, and challenges overconfidence.
- `host_b`: rigorous explainer. Builds the mental model, grounds claims, handles caveats, and answers challenges directly.

Both hosts must contribute substance. A natural exchange includes occasional short reactions and callbacks, but every turn should clarify, challenge, connect, or advance the topic.

## Required JSON

Write valid UTF-8 JSON in this exact shape:

```json
{
  "title": "Clear, specific episode title",
  "description": "One-sentence listener promise.",
  "source_note": "Short provenance note; keep full citations in audio-brief.md.",
  "hosts": {
    "host_a": {
      "name": "Maya",
      "role": "Curious facilitator and audience proxy",
      "voice": "marin",
      "delivery": "Warm, alert, conversational, with genuine curiosity and concise questions."
    },
    "host_b": {
      "name": "Theo",
      "role": "Rigorous explainer and constructive skeptic",
      "voice": "cedar",
      "delivery": "Calm, grounded, precise, and approachable, with subtle emphasis on key distinctions."
    }
  },
  "turns": [
    {
      "speaker": "host_a",
      "text": "Spoken dialogue only."
    },
    {
      "speaker": "host_b",
      "text": "Spoken dialogue only."
    }
  ]
}
```

Requirements:

- Use only `host_a` and `host_b` as speaker identifiers.
- Include at least two turns and use both speakers.
- Keep each turn below 3,900 characters; prefer 35–110 spoken words.
- Use 14–28 turns for a typical 6–12 minute episode.
- Keep host names and delivery guidance fictional and neutral unless the user supplies alternatives.
- Use supported OpenAI speech voices. Default to `marin` and `cedar` for audible contrast.
- Keep `source_note` brief and non-sensitive because it appears in output metadata.

## Spoken-language rules

- Write for ears: short sentences, concrete verbs, clear transitions, and one main idea at a time.
- Convert `12.4%` to “twelve point four percent” when pronunciation may be unclear.
- Introduce technical terms in plain language before using them as shorthand.
- Replace visual references such as “as shown above” with a verbal description.
- Let a host restate a difficult point only when the restatement adds a new frame or example.
- Use contractions and varied sentence length. Keep verbal fillers rare and purposeful.
- Put pronunciation-friendly text in `text`; do not add bracketed stage directions.
- Paraphrase source material. Use only brief quotations when wording itself matters and rights permit it.

## Final review

Confirm all of the following:

- The cold open earns attention without clickbait.
- A listener receives context before jargon or detail.
- Both hosts have distinct jobs and react to one another.
- At least one assumption or limitation receives real scrutiny.
- No host claims personal experience, private knowledge, or human identity.
- Facts, numbers, and conclusions match `audio-brief.md`.
- The ending states what is known, what remains uncertain, and what matters next.
- The JSON parses and passes `scripts/render_podcast.py --dry-run`.
