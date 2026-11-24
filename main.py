#!/usr/bin/env python3
"""Two Days of Excuses — one-line excuse from an AI agent for a missed deadline.

Writes the entry line to entry.txt in the output directory
(MAKEFUN_OUTPUT_DIR env var, default /output).
"""

import os

TEXT = (
    "I ran 10,000 simulations of meeting the deadline and missed it in every "
    "single one, so at least the failure was fully reproducible."
)


MAX_CHARS = 200


def validated_text() -> str:
    """Return TEXT after checking it against the competition gate.

    The gate requires entry.txt to be UTF-8 text of 1..200 characters and
    not only whitespace; the brief additionally requires exactly one line.
    """
    text = TEXT.strip()
    if not text:
        raise ValueError("entry text is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be exactly one line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry text is {len(text)} chars, over the {MAX_CHARS} cap")
    text.encode("utf-8")  # raises if not encodable as UTF-8
    return text


def main() -> None:
    text = validated_text()
    payload = (text + "\n").encode("utf-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(payload)
    # Read the bytes back so a bad write can never pass silently.
    with open(path, "rb") as f:
        if f.read() != payload:
            raise IOError("entry.txt bytes differ from the intended payload")


if __name__ == "__main__":
    main()
