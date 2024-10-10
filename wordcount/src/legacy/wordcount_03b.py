"""
Refactor to use a named tuple.
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


def main():
    counts = Counts.from_bytes(sys.stdin.buffer.read())
    print(counts.lines, counts.words, counts.bytes)
