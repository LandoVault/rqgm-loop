"""Mechanical helper for the 2026-09-25 RQGM meta-run (stdlib only).

The workflow's LLM roles propose and judge; this script does the bookkeeping they
must not do by hand: content-addressed snapshots of the target files, exact-anchor
diff application, word caps, and a stale-base guard before promotion.

  python meta_tool.py snapshot                    -> {"hash": ...}  (snapshot of the worktree targets)
  python meta_tool.py apply VARIANT.json BASE     -> {"ok", "hash", "errors", "words", "caps_ok", "diff"}
  python meta_tool.py promote NEW BASE            -> copies snapshot NEW into the worktree if it still equals BASE
  python meta_tool.py words HASH                  -> word counts of a snapshot

VARIANT.json: {"id": "r3-a", "edits": [{"file": "skills/rqgm-loop/SKILL.md", "old": "...", "new": "..."}]}
Each `old` must occur exactly once in the file at the time it is applied; otherwise the
variant is an ERROR (not a merit loss). Word counts use str.split(), like `wc -w`.
Text is normalized to LF (the worktree may be checked out with CRLF).
"""
import difflib
import hashlib
import json
import os
import sys

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(RUN))
SNAP = os.path.join(RUN, "snapshots")
DIFFS = os.path.join(RUN, "diffs")
CONFIG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "caps.json"), encoding="utf-8"))
TARGETS = list(CONFIG["caps"].keys())


def lf(s):
    return s.replace("\r\n", "\n")


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8", newline="") as f:
        return lf(f.read())


def digest(texts):
    h = hashlib.sha256()
    for rel in TARGETS:
        h.update(rel.encode() + b"\0" + texts[rel].encode("utf-8") + b"\0")
    return h.hexdigest()[:12]


def store(texts):
    hid = digest(texts)
    d = os.path.join(SNAP, hid)
    if not os.path.isdir(d):
        for rel in TARGETS:
            p = os.path.join(d, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(texts[rel])
    return hid


def load(hid):
    d = os.path.join(SNAP, hid)
    if not os.path.isdir(d):
        raise SystemExit(json.dumps({"ok": False, "errors": [f"unknown snapshot {hid}"]}))
    return {rel: read(d, rel) for rel in TARGETS}


def words(texts):
    return {rel: len(texts[rel].split()) for rel in TARGETS}


def caps_report(w):
    over = {rel: (w[rel], cap) for rel, cap in CONFIG["caps"].items() if w[rel] > cap}
    return (not over), over


def cmd_snapshot():
    texts = {rel: read(REPO, rel) for rel in TARGETS}
    hid = store(texts)
    ok, over = caps_report(words(texts))
    print(json.dumps({"hash": hid, "words": words(texts), "caps_ok": ok, "over": over}))


def cmd_apply(vpath, base):
    v = json.load(open(vpath, encoding="utf-8"))
    texts = load(base)
    errors = []
    for i, e in enumerate(v.get("edits", [])):
        rel = e.get("file")
        if rel not in TARGETS:
            errors.append(f"edit {i}: file {rel!r} is not a target")
            continue
        old, new = lf(e.get("old", "")), lf(e.get("new", ""))
        n = texts[rel].count(old) if old else 0
        if not old:
            errors.append(f"edit {i}: empty anchor")
        elif n != 1:
            errors.append(f"edit {i}: anchor occurs {n} times in {rel} (must be exactly 1)")
        else:
            texts[rel] = texts[rel].replace(old, new, 1)
    if not v.get("edits"):
        errors.append("no edits")
    if errors:
        print(json.dumps({"ok": False, "class": "ERROR", "errors": errors, "variant": v.get("id")}))
        return
    new = store(texts)
    w = words(texts)
    ok, over = caps_report(w)
    base_texts = load(base)
    os.makedirs(DIFFS, exist_ok=True)
    dpath = os.path.join(DIFFS, f"{base}-{new}.diff")
    with open(dpath, "w", encoding="utf-8", newline="") as f:
        for rel in TARGETS:
            f.writelines(difflib.unified_diff(base_texts[rel].splitlines(True), texts[rel].splitlines(True),
                                              fromfile=f"A/{rel}", tofile=f"B/{rel}", n=3))
    bw = words(base_texts)
    print(json.dumps({"ok": ok, "class": "OK" if ok else "CAP", "hash": new, "base": base, "words": w,
                      "words_delta": {rel: w[rel] - bw[rel] for rel in TARGETS}, "caps_ok": ok, "over": over,
                      "diff": os.path.relpath(dpath, RUN).replace("\\", "/"), "variant": v.get("id")}))


def cmd_promote(new, base):
    current = {rel: read(REPO, rel) for rel in TARGETS}
    if digest(current) != base:
        print(json.dumps({"ok": False, "class": "STALE", "errors": [f"worktree is {digest(current)}, expected base {base}"]}))
        return
    texts = load(new)
    for rel in TARGETS:
        with open(os.path.join(REPO, rel), "w", encoding="utf-8", newline="") as f:
            f.write(texts[rel])
    print(json.dumps({"ok": True, "promoted": new, "from": base, "words": words(texts)}))


def cmd_words(hid):
    w = words(load(hid))
    ok, over = caps_report(w)
    print(json.dumps({"hash": hid, "words": w, "caps_ok": ok, "over": over}))


if __name__ == "__main__":
    a = sys.argv[1:]
    {"snapshot": lambda: cmd_snapshot(), "apply": lambda: cmd_apply(a[1], a[2]),
     "promote": lambda: cmd_promote(a[1], a[2]), "words": lambda: cmd_words(a[1])}[a[0]]()
