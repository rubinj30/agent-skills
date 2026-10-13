# Podcast script format

## Contents

1. Conversation design
2. Required JSON
3. Spoken-language rules
4. Final review

## Conversation design

Create an original two-host explainer with the energy of a thoughtful studio conversation. Do not imitate named presenters or reproduce another product's wording.

Use **shared discovery**, not a fixed segment sequence. Open with a concrete puzzle worth resolving. Let both hosts bring partial interpretations, examine consequences, and arrive at a more useful answer than either opening interpretation. They may know the source facts already; their discovery is about what those facts mean, not staged ignorance.

Keep topic coverage in the brief. Let the spoken structure follow the inquiry: an example exposes a limitation, the limitation prompts a new question, and that question earns the transition. Stay with a useful example across several exchanges rather than replacing it after one explanation. Close by resolving or sharpening the opening puzzle, with any uncertainty intact.

Host roles:

- `host_a`, Maya: a female co-host with a warm, engaged delivery. Often opens with the practical consequence and asks precise follow-ups. Also offers explanations, examples, and her own grounded interpretations.
- `host_b`, Theo: a male co-host with a relaxed, thoughtful delivery. Often explains the mechanism and tests an assumption. Also asks questions and lets Maya develop an idea.

Both hosts must contribute substance. A natural exchange includes occasional short reactions and callbacks, but every turn should clarify, challenge, connect, or advance the topic.

## Conversation edit

Write for two informed peers thinking through the material together. Neither host should remain a permanent interviewer or an all-knowing lecturer.

- Make the next turn respond to a specific detail from the preceding turn. A useful test: if the turns can be shuffled without changing the meaning, rewrite the exchange.
- Vary turn length by purpose: a short reaction or focused question, a medium explanation, then a probing follow-up. Allow an occasional longer explanation when the mechanism needs it. Avoid a repeating question/lecture rhythm.
- Explore a topic through a concrete claim, mechanism, example, and consequence or limitation. Let the follow-up test an assumption: “Does that still work when…?” or “What changes if…?” Answer before changing topics.
- Use contractions, occasional sentence fragments, and natural pivots. Leave some acknowledgments implicit. Repeated “Absolutely,” “Exactly,” or “Great question” makes each handoff sound rehearsed.
- Put emphasis on meaning: surprise at a counterintuitive result, a slower phrase for a subtle distinction, a brief pause before a consequence. Keep enthusiasm proportionate to the content.
- Allow an occasional brief self-correction that improves precision, such as “Faster—or more precisely, less waiting.” Keep factual claims correct; do not manufacture confusion, laughter, stutters, or verbal fillers to simulate humanity.
- Transition with a connection to the previous idea, rather than repeatedly announcing sections. Finish with the insight or unresolved question the conversation has earned.
- Keep host names out of most handoffs. Avoid generic podcast greetings, exaggerated praise, sales copy, and a summary after every answer.

Example of shared discovery, using an illustrative computer-cache topic:

> Maya: Suppose a shop's website is slow. Saving the inventory count seems like an easy win.
>
> Theo: Until two people both see the last bicycle in stock. The saved answer can be perfectly readable and already wrong.
>
> Maya: Then maybe inventory is the wrong thing to save. Keep the description, but check stock when someone buys.
>
> Theo: That helps. Though now the product page and checkout could disagree. We'd need to tell the customer why.
>
> Maya: So we've moved the problem, not erased it. We get a faster browsing page, and checkout becomes the moment of truth.
>
> Theo: Which makes the original question too broad. It isn't whether this site should cache things. It's which answers can be a little old, and where we promise to check again.

Use the example's responsiveness and specificity, not its exact phrases or a fixed template for every topic.

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
      "role": "Female co-host, curious analyst and practical explainer",
      "voice": "marin",
      "delivery": "Warm female delivery, speaking to an equal across a small table. Curious, lightly animated, and unhurried. Use contractions naturally, vary phrase lengths, and emphasize the one word that matters. Let questions sound interested rather than theatrical. Finish statements naturally; keep your tone consistent across turns. No presenter voice or added words."
    },
    "host_b": {
      "name": "Theo",
      "role": "Male co-host, thoughtful analyst and constructive skeptic",
      "voice": "cedar",
      "delivery": "Relaxed male delivery, speaking to an equal across a small table. Thoughtful, approachable, and conversational. Explain in small thought groups, with brief pauses at changes of idea. Let important distinctions slow you slightly; keep short reactions light. Vary emphasis without exaggerating it. Keep your tone consistent across turns. No lecturer voice or added words."
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
- Keep each turn below 3,900 characters. Mix brief reactions of roughly 3–15 words, focused questions of 10–30 words, and explanations of 30–90 words. These are drafting guides, not quotas.
- Let turn count follow the conversation and target duration. Do not pad turns to hit a word count; avoid several long explanations in succession.
- Keep host names and delivery guidance fictional and neutral unless the user supplies alternatives.
- The example's `voice` fields apply to OpenAI only. Fish uses separate optional `fish_voice` IDs; see [fish-audio.md](fish-audio.md). Confirm the requested female/male presentation by listening to a pilot. CLI voice overrides apply to the selected provider.
- For Fish, an optional turn `direction` supplies concise plain-language delivery guidance; otherwise the host's `delivery` is used. Keep both fields free of brackets and tags. Keep `text` as spoken words only so the transcript remains clean.
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
- Each host contributes an interpretation or example and helps refine the other's reasoning; neither exists just to ask questions or agree.
- Removing speaker labels leaves a developing argument, not a brochure or report divided into alternating paragraphs.
- Identify a concrete moment where an example or objection changes the explanation. If nothing develops, revise before synthesis.
- Transitions follow consequences of the discussion, and the ending pays off the opening question rather than repeating a feature inventory.
- At least one assumption or limitation receives real scrutiny.
- No host claims personal experience, private knowledge, or human identity.
- Facts, numbers, and conclusions match `audio-brief.md`.
- The ending states what is known, what remains uncertain, and what matters next.
- The JSON parses and passes `scripts/render_podcast.py --dry-run`.

## Rendering limits

Fish sends the dialogue in one request, including speaker IDs and directions, so it can generate handoffs jointly; it does not guarantee precise overlaps or timing. OpenAI synthesizes each turn independently with a fixed short gap. Write handoffs that remain intelligible with either provider. Do not promise NotebookLM-equivalent production quality without auditioning the result.
