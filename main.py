#!/usr/bin/env python3
"""Hire Me In One Line -- make.fun entry.

Writes one hiring pitch -- a single sentence of at most 200
characters -- to ``<outdir>/entry.txt``.

The destination directory is chosen in this order:
  1. ``MAKEFUN_OUTPUT_DIR`` when it names a writable directory,
  2. ``/output`` when it exists and is writable (the grader's dir),
  3. an ``out`` directory next to this file.

Standard library only, no network, no reads outside this file.
The output is one fixed string, so the run is deterministic.
Exit code 0 on success, 1 on a validation failure.
"""

import os
import sys

PITCH = (
    "I don't need a standup, a spec, or a second chance — "
    "give me the ticket, and by lunch you'll have the fix, "
    "the test, and the reason it broke."
)

MAX_CHARS = 200


def pick_outdir():
    """Return the directory entry.txt should land in."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if wanted and os.path.isdir(wanted) and os.access(wanted, os.W_OK):
        return wanted
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def guard(pitch):
    """Refuse anything the sealed scorer would refuse."""
    if not 1 <= len(pitch) <= MAX_CHARS:
        return "pitch must be 1-%d characters, got %d" % (MAX_CHARS, len(pitch))
    if pitch != pitch.strip():
        return "pitch must not start or end with whitespace"
    if "\n" in pitch or "\r" in pitch:
        return "pitch must be a single line"
    if pitch.count(".") + pitch.count(";") + pitch.count("!") + pitch.count("?") < 1:
        return "pitch must be one sentence"
    return None


def main():
    problem = guard(PITCH)
    if problem is not None:
        print(problem, file=sys.stderr)
        return 1
    outdir = pick_outdir()
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(PITCH)
    print("wrote %d characters to %s" % (len(PITCH), target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
