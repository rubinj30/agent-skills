# Design it twice

Use this process only after a candidate is selected and the interface is consequential or difficult to reverse.

## Frame

Write the behavior, constraints, dependencies, invariants, and failure modes that every design must satisfy. Keep proposed solutions out of the frame.

## Produce alternatives

Create at least two materially different interfaces. If isolated or parallel workers are available and the task justifies their cost, give each the same frame but a different design objective:

- minimize interface concepts;
- optimize the dominant caller;
- maximize substitutability at a real external seam.

Each design must specify:

1. operations and types;
2. invariants, ordering, and errors;
3. caller example;
4. implementation hidden behind the seam;
5. dependency and adapter strategy;
6. migration path;
7. leverage and tradeoffs.

## Compare

Compare depth, locality, test surface, common-case ergonomics, misuse risk, and migration cost. Recommend one design or an explicit hybrid. Record why the rejected designs lost so the choice does not depend on memory.
