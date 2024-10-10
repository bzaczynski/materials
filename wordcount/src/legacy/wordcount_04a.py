"""
Format the numbers according to the maximum number of digits in the counts.
"""

import sys
from typing import NamedTuple


class Counts(NamedTuple):
    lines: int
    words: int
    bytes: int

    @classmethod
    def from_bytes(cls, raw_text):
        text = raw_text.decode("utf-8")
        return cls(
            lines=text.count("\n"),
            words=len(text.split()),
            bytes=len(raw_text),
        )

    @property
    def max_digits(self):
        return len(str(max(self)))


def main():
    counts = Counts.from_bytes(sys.stdin.buffer.read())
    print(
        f"{counts.lines:>{counts.max_digits}} "
        f"{counts.words:>{counts.max_digits}} "
        f"{counts.bytes:>{counts.max_digits}}"
    )
