"""
Refactor, introduce a helper function.
"""

import sys
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from enum import IntFlag, auto
from functools import cached_property
from pathlib import Path
from typing import NamedTuple


class SelectedCounts(IntFlag):
    NONE = 0
    LINES = auto()
    WORDS = auto()
    BYTES = auto()
    DEFAULT = LINES | WORDS | BYTES


class Arguments(Namespace):
    @cached_property
    def selected_counts(self):
        selected = self.lines | self.words | self.bytes
        return selected or SelectedCounts.DEFAULT  # Short-circuit evaluation, "or"


class Counts(NamedTuple):
    lines: int = 0
    words: int = 0
    bytes: int = 0

    def max_digits(self, selected_counts):
        return len(str(max(self.numbers(selected_counts))))

    def __add__(self, other):
        return Counts(
            lines=self.lines + other.lines,
            words=self.words + other.words,
            bytes=self.bytes + other.bytes,
        )

    def as_string(self, max_digits, selected_counts):
        return " ".join(
            f"{number:>{max_digits}}"
            for number in self.numbers(selected_counts)
        )

    def numbers(self, selected_counts):
        return [
            getattr(self, flag.name.lower())
            for flag in SelectedCounts
            if flag & selected_counts
        ]


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
            )
        )


def main():
    args = parse_args()
    if len(args.paths) > 0:
        file_infos = [FileInfo.from_path(path) for path in args.paths]
    else:
        file_infos = [FileInfo.from_path(Path("-"))]
    display(file_infos, args.selected_counts)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    for flag in SelectedCounts:
        parser.add_argument(
            f"--{flag.name.lower()}",
            action="store_const",
            const=flag,
            default=SelectedCounts.NONE,
        )
    return parser.parse_args(namespace=Arguments())


def display(file_infos, selected_counts):
    total_counts = sum((info.counts for info in file_infos), Counts())
    max_digits = total_counts.max_digits(selected_counts)
    for info in file_infos:
        line = info.counts.as_string(max_digits, selected_counts)
        if info.path == Path("-"):
            print(line)
        elif not info.path.exists():
            print(line, info.path, "(no such file or directory)")
        elif info.path.is_dir():
            print(line, f"{info.path}/ (is a directory)")
        else:
            print(line, info.path)
    if len(file_infos) > 1:
        print(total_counts.as_string(max_digits, selected_counts), "total")
