"""Merge half-open integer intervals. See spec.md."""


def merge(intervals):
    for a, b in intervals:
        if a > b:
            raise ValueError(f"bad interval {(a, b)}")
    intervals.sort()
    out = []
    for a, b in intervals:
        if out and a < out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out
