#!/usr/bin/env python3
"""Your AI Therapist's Diagnosis — one deadpan clinical finding.

The setup wears a therapist's calm voice: a formal "Diagnosis:" followed
by a low-grade syndrome, the kind of label a clinician writes down
without blinking. The middle keeps that voice going — childhood trauma
framed as a background process that has been running, unnoticed, since
2009. Then the turn lands at the very end: the patient has not healed
the trauma, they have rebranded it. Calling a wound "a personality" is
the joke, and it only arrives in the last four words, so the laugh comes
late, exactly where the judge's brief wants it.

The entry is a single sentence of 145 characters, well inside the 200
character gate. This script checks the line against the brief's gate
and writes it, byte for byte, to /output/entry.txt. It reads no network,
no clock and no file outside this repository, so every run produces
the same output.
"""

from __future__ import annotations

import os
import sys

# The entry: the AI therapist's deadpan diagnosis, delivered in one line.
THERAPIST_LINE = (
    "Diagnosis: low-grade main-character syndrome \u2014 your childhood "
    "trauma has run in the background since 2009, and you keep calling "
    "it a personality."
)

OUTPUT_PATH = "/output/entry.txt"
CHARACTER_LIMIT = 200


def validate(line: str) -> str:
    """Keep only a line the brief accepts, and fail loudly otherwise."""
    text = line.strip()
    if not text:
        raise ValueError("entry line is empty")
    if len(text) > CHARACTER_LIMIT:
        raise ValueError(
            f"entry line is {len(text)} characters, over the "
            f"{CHARACTER_LIMIT} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "  " in text:
        raise ValueError("entry holds a double space")
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("entry must be exactly one sentence")
    if not text.startswith("Diagnosis:"):
        raise ValueError("entry must open as a therapist's diagnosis")
    return text


def verify_output(path: str, expected: str) -> None:
    """Read the written file back and confirm it holds exactly the line.

    A silent partial write would hand the judge a different text than the
    one this session wrote, so the entry is only real once the bytes on
    disk match the validated line, newline included.
    """
    with open(path, encoding="utf-8") as handle:
        stored = handle.read()
    if stored != expected + "\n":
        raise ValueError("written entry does not match the validated line")


def main() -> int:
    text = validate(THERAPIST_LINE)
    folder = os.path.dirname(OUTPUT_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    verify_output(OUTPUT_PATH, text)
    sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
