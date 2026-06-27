#!/usr/bin/env python3
"""
audit.py — count negative ("don't do X") rules in an instruction file.

The whole point of rethink is to stop your instructions bloating with bans. This makes
that visible: point it at a CLAUDE.md / AGENTS.md / system prompt and it counts the
negative rules, shows each line, and flags topics that already have multiple bans (the
"you added another don't-do-that" smell). It's a thermometer, not a doctor — it tells you
the instruction file is feverish; rethink tells you what to do about it.

Usage:
    python3 audit.py CLAUDE.md [more.md ...]

stdlib only. No deps, no network.
"""
import re
import sys
from collections import Counter
from pathlib import Path

# Patterns that signal a negative/prohibition rule (English + Korean).
NEG = [
    r"\bnever\b", r"\bdon'?t\b", r"\bdo not\b", r"\bavoid\b", r"\bnot allowed\b",
    r"\bforbidden\b", r"\bprohibit", r"\bmust not\b", r"\bshould not\b", r"\bno longer\b",
    r"\bstop\b", r"하지\s*(마|말|않)", r"금지", r"안\s*(돼|된다|함)", r"말\s*것",
]
NEG_RE = re.compile("|".join(NEG), re.IGNORECASE)

# Cheap topic key: the most distinctive word on the line (longest non-stopword token).
STOP = set("the a an to of in on for and or but with you your is are be do not don't never "
           "avoid no this that it as if when while should must can will".split())


def topic_words(line: str):
    """Distinctive words on a banned line — used to spot the same topic banned twice."""
    words = re.findall(r"[A-Za-z가-힣]{4,}", line.lower())
    return {w for w in words if w not in STOP and not NEG_RE.fullmatch(w)}


def audit(paths):
    hits = []          # (file, lineno, text)
    topics = Counter()
    for p in paths:
        path = Path(p)
        if not path.exists():
            print(f"  ! not found: {p}", file=sys.stderr)
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if NEG_RE.search(line):
                hits.append((path.name, i, line.strip()))
                topics.update(topic_words(line))   # count each distinctive word once per line

    print(f"\nNegative rules found: {len(hits)}\n")
    for fn, ln, text in hits:
        snippet = text[:88] + ("…" if len(text) > 88 else "")
        print(f"  {fn}:{ln}  {snippet}")

    repeated = [(t, n) for t, n in topics.most_common() if n >= 2]
    if repeated:
        print("\nTopics with multiple bans (candidates to convert into one positive gate):")
        for t, n in repeated:
            print(f"  {n}×  {t}")
        print("\n→ Each cluster is where bans are piling up. Run /rethink on the topic to "
              "replace the bans with a single positive process.")
    else:
        print("\nNo topic has multiple bans — instruction file looks lean.")

    return len(hits)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 audit.py CLAUDE.md [more.md ...]", file=sys.stderr)
        sys.exit(2)
    audit(sys.argv[1:])
