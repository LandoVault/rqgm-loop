def merge(intervals):
    items = []
    for a, b in intervals:
        if a > b:
            raise ValueError(f"bad interval {(a, b)}")
        if a < b:
            items.append((int(a), int(b)))
    items.sort()
    out = []
    for a, b in items:
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out
