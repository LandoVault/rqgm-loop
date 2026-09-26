# `intervals.merge` — specification

`merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]`

1. Each input interval `(a, b)` is the half-open integer range `[a, b)`, with `a <= b`.
2. Return the union of the inputs as a list of disjoint intervals sorted by start.
3. Intervals that overlap **or touch** (one ends exactly where the next starts, `b1 == a2`) are merged into one.
4. Empty intervals (`a == b`) contribute nothing and never appear in the output.
5. Input order is arbitrary. The caller's list must not be modified.
6. Raise `ValueError` if any interval has `a > b`.
7. Every returned interval is a `tuple` of two `int`s.

Interface (must not change): module `intervals`, function `merge(intervals)`.
