"""
There is code duplication, let's refactor it before moving on.
"""

import sys
from pathlib import Path
from typing import NamedTuple


class Counts(NamedTuple):
    lines: int = 0
    words: int = 0
    bytes: int = 0

    @property
    def max_digits(self):
        return len(str(max(self)))  # Use max(self) thanks to NamedTuple

    def __add__(self, other):
        return Counts(
            lines=self.lines + other.lines,
            words=self.words + other.words,
            bytes=self.bytes + other.bytes,
        )

    def __str__(self):
        return (
            f"{self.lines:>{self.max_digits}} "
            f"{self.words:>{self.max_digits}} "
            f"{self.bytes:>{self.max_digits}}"
        )


def main():
    if len(sys.argv) > 1:
        paths = [Path(arg) for arg in sys.argv[1:]]
    else:
        paths = [Path("-")]
    total_counts = Counts()
    for path in paths:
        try:
            if path.name == "-":
                raw_text = sys.stdin.buffer.read()
            else:
                raw_text = path.read_bytes()
            text = raw_text.decode("utf-8")
            counts = Counts(
                lines=text.count("\n"),
                words=len(text.split()),
                bytes=len(raw_text),
            )
            total_counts += counts
            if path.name != "-":
                print(counts, path)
            else:
                print(counts)
        except IsADirectoryError:
            print(f"0 0 0 {path}/ (is a directory)")
        except FileNotFoundError:
            print(f"0 0 0 {path} (no such file or directory)")
    if len(paths) > 1:
        print(total_counts, "total")
