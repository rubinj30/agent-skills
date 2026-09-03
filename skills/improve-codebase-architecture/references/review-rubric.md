# Architecture review rubric

Score each category from 0 to 3. Write one evidence sentence per score; never rank from intuition alone.

| Category | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Recurrence | One-off or dormant | Plausible future cost | Repeated current work | Active hotspot across history |
| Interface burden | Already small and explicit | Minor caller knowledge | Many caller rules | Callers reconstruct the implementation |
| Locality gain | Change remains scattered | Small consolidation | Most related change concentrates | One module becomes the clear owner |
| Test leverage | No meaningful improvement | Some setup reduction | Observable tests replace internal mocks | One interface covers critical workflows |
| Behavior confidence | Poorly understood | Partial tests or docs | Clear invariants and coverage | Reconciled implementation, tests, and runtime evidence |
| Migration cost | Large, coupled rewrite | Multi-stage and risky | Bounded migration | Small reversible slice |

Calculate:

`priority = recurrence + interface burden + locality gain + test leverage + behavior confidence + migration cost`

Interpretation:

- **15–18 — Strong:** recommend now, subject to repository constraints.
- **10–14 — Worth exploring:** design the seam before committing.
- **6–9 — Speculative:** retain only if it exposes an important uncertainty.
- **0–5 — Reject:** omit from the final candidate list.

The migration-cost score is higher when migration is safer and cheaper. A high total never overrides an ADR, security requirement, public compatibility promise, or explicit user constraint.

## Evidence standards

Strong evidence includes:

- repeated co-changes in git history;
- multiple callers carrying the same rule;
- integration defects caused by split ownership;
- tests coupled to private implementation details;
- documented operational or onboarding pain;
- a trace showing framework or infrastructure details crossing several callers.

Weak evidence includes file size alone, personal style preference, speculative future reuse, unfamiliarity with a framework, or a diagram that looks untidy.
