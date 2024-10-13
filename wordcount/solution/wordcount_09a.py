"""
Replace sys.argv[1:] with argparse.
"""

import sys
from argparse import ArgumentParser
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
            return cls(path, Counts())
        text = raw_text.decode("utf-8")
        return cls(
            path,
            Counts(
                lines=text.count("\n"),
                words=len(text.split()),
                bytes=len(raw_text),
            ),
        )


def main():
    args = parse_args()
    if len(args.paths) > 0:
        file_infos = [FileInfo.from_path(path) for path in args.paths]
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


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    return parser.parse_args()
