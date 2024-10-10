"""
Use consistent formatting by delaying the moment of printing, and collecting files stats.
"""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple


class Counts(NamedTuple):
    lines: int = 0
    words: int = 0
    bytes: int = 0

    @property
    def max_digits(self):
        return len(str(max(self)))

    def __add__(self, other):
        return Counts(
            lines=self.lines + other.lines,
            words=self.words + other.words,
            bytes=self.bytes + other.bytes,
        )

    def as_string(self, max_digits):
        return (
            f"{self.lines:>{max_digits}} "
            f"{self.words:>{max_digits}} "
            f"{self.bytes:>{max_digits}}"
        )


@dataclass(frozen=True)
class FileInfo:
    path: Path
    counts: Counts

    @classmethod
    def from_path(cls, path):
        if path.name == "-":
            raw_text = sys.stdin.buffer.read()
        elif path.is_file():
            raw_text = path.read_bytes()
        else:
            return cls(path, Counts(0, 0, 0))
        text = raw_text.decode("utf-8")
        return cls(
            path,
            Counts(
                lines=text.count("\n"),
                words=len(text.split()),
                bytes=len(raw_text),
            )
        )


def main():
    if len(sys.argv) > 1:
        file_infos = [FileInfo.from_path(Path(arg)) for arg in sys.argv[1:]]
    else:
        file_infos = [FileInfo.from_path(Path("-"))]
    total_counts = sum((info.counts for info in file_infos), Counts())
    max_digits = total_counts.max_digits
    for info in file_infos:
        line = info.counts.as_string(max_digits)
        if info.path == Path("-"):
            print(line)
        elif not info.path.exists():
            print(line, info.path, "(no such file or directory)")
        elif info.path.is_dir():
            print(line, f"{info.path}/ (is a directory)")
        else:
            print(line, info.path)
    if len(file_infos) > 1:
        print(total_counts.as_string(max_digits), "total")
