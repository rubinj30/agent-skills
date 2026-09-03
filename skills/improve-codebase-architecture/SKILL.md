---
name: improve-codebase-architecture
description: Inspect an existing codebase for evidence-backed architectural friction and rank high-leverage refactoring opportunities that improve module depth, change locality, interfaces, and testability. Use for architecture reviews, refactoring strategy, module consolidation, seam placement, tangled dependencies, repeated logic, or codebases that are difficult for humans or coding agents to navigate.
---

# Improve Codebase Architecture

Find the smallest architectural changes that remove the most recurring complexity. Ground every recommendation in code, tests, history, or documented constraints.

## Vocabulary

- **Module:** code with an interface and an implementation, at any scale.
- **Interface:** everything callers must know, including invariants, ordering, errors, configuration, and performance constraints.
- **Depth:** useful behavior hidden behind a small interface.
- **Seam:** a place where behavior can vary without changing callers.
- **Adapter:** a concrete implementation placed at a seam.
- **Leverage:** capability gained by callers per interface concept learned.
- **Locality:** how tightly related knowledge, change, and verification stay together.

Use this vocabulary consistently so recommendations remain comparable.

## Workflow

### 1. Establish the contract

1. Read repository instructions, the root README, package manifests, architecture documents, domain glossaries, ADRs, and the relevant plans.
2. Inspect `git status` and preserve unrelated or uncommitted work.
3. Determine whether the user requested review, design, or implementation. Treat review and design as read-only.
4. Use the user's named subsystem as scope. Otherwise, inspect meaningful commit history and recurring change paths to locate current hotspots before scanning broadly.

Complete this step when the scope, current behavior, constraints, and permitted side effects are explicit.

### 2. Trace behavior, not filenames

Follow one or more real workflows from entry point to observable result. Read the implementation and tests at each hop. Record concrete evidence of:

- one behavior scattered across many modules;
- repeated policy or translation logic;
- shallow pass-through modules whose interfaces expose nearly all their implementation;
- broker, database, transport, framework, or runtime details leaking across a seam;
- hidden ordering, state, retry, or failure rules callers must remember;
- tests that mock internals yet miss integration failures;
- a change hotspot whose edits repeatedly span the same file cluster;
- cycles, inconsistent ownership, or parallel state models.

Apply the deletion test: imagine removing a suspected shallow module. A useful module forces complexity to reappear in multiple callers; a weak module makes complexity disappear with it.

### 3. Form candidates

Propose 3–5 candidates at most. For each candidate:

1. Name the user or system behavior it improves.
2. Identify the present interface burden and the exact files involved.
3. Place one clear seam and state what implementation moves behind it.
4. Explain the resulting leverage, locality, and test surface.
5. Describe migration risk, behavior that must remain invariant, and the smallest reversible first slice.

Prefer consolidating proven coupling over inventing abstractions for hypothetical reuse. Introduce a seam when at least two meaningful adapters exist, commonly production and test implementations.

### 4. Rank with evidence

Read [references/review-rubric.md](references/review-rubric.md) completely and score every candidate. Reject a candidate when evidence is weak, its interface would grow, behavior preservation is unclear, or migration cost exceeds the recurring friction.

Select one top recommendation. A review that produces no defensible candidate should say so.

### 5. Deliver the review

Use this compact shape for each candidate:

1. **Candidate and strength:** `Strong`, `Worth exploring`, or `Speculative`.
2. **Files and evidence:** specific paths plus the observed friction.
3. **Seam:** where the new or deepened module's interface lives.
4. **Change:** what moves behind the interface.
5. **Payoff:** leverage, locality, and test improvement.
6. **Risk and first slice:** preserved behavior, migration risk, and reversible starting point.

End with the top recommendation and why it outranks the others. Ask which candidate the user wants to design or implement only after providing a decisive recommendation.

For three or more candidates whose relationships are hard to understand in prose, create a self-contained HTML report in the operating-system temp directory. Keep generated review artifacts outside the repository unless the user asks to retain them.

## Detailed design

When the user selects a candidate, define the proposed interface completely: operations, inputs, outputs, invariants, ordering, errors, configuration, and performance expectations. State what becomes internal and which callers change.

For a consequential or hard-to-reverse interface, read [references/design-it-twice.md](references/design-it-twice.md) and compare materially different designs before choosing.

## Implementation

Implement only when the user authorizes code changes.

1. Capture current observable behavior with focused tests.
2. Introduce the selected interface in a reversible slice.
3. Move behavior behind it without changing unrelated behavior.
4. Replace old call paths rather than permanently layering old and new abstractions.
5. Test through the new interface and retain necessary end-to-end coverage.
6. Remove obsolete modules and tests only after every caller is migrated and verification passes.
7. Report behavior preserved, files changed, validation evidence, and remaining risk.

Keep cleanup proportional to the selected candidate. A refactor is complete when the recurring complexity is more local, the caller interface is smaller or clearer, and tests exercise observable behavior through the intended seam.
