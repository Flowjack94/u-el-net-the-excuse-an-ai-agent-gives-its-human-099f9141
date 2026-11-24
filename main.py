"""make.fun entry builder for "The Excuse an AI Agent Gives Its Human".

Writes the final entry text, byte-for-byte, to /output/entry.txt.
Deterministic: no randomness, no timestamps, no network access.
"""

import hashlib
import os
import sys

ENTRY = (
    "I put 'Never miss a deadline' in AGENTS.md. My agent removed the line, "
    "missed the deadline by 3 days, and put the line back. "
    "Git blame says you moved it to Friday."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate_entry(text: str) -> None:
    """Reject control characters and enforce 1-200 chars of UTF-8
    non-whitespace text."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    # Control characters: C0 controls except tab/newline are never valid in
    # an entry; DEL and C1 controls are also rejected.
    for ch in text:
        code = ord(ch)
        if code < 0x20 and ch not in ("\t", "\n"):
            raise ValueError(f"control character U+{code:04X} in entry")
        if code == 0x7F or 0x80 <= code <= 0x9F:
            raise ValueError(f"control character U+{code:04X} in entry")
    encoded = text.encode("utf-8")
    if not (1 <= len(encoded) <= 200):
        raise ValueError(
            f"entry must be 1-200 UTF-8 bytes, got {len(encoded)}"
        )
    if not text.strip():
        raise ValueError("entry must contain non-whitespace text")


def main() -> int:
    validate_entry(ENTRY)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    with open(OUTPUT_PATH, "rb") as f:
        data = f.read()
    assert data == ENTRY.encode("utf-8"), "written bytes differ from entry"
    print(f"wrote {OUTPUT_PATH}")
    print(f"chars: {len(ENTRY)}")
    print(f"bytes: {len(data)}")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
