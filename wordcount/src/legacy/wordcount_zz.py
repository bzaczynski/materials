import re
import sys
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from enum import IntFlag, auto
from functools import cached_property
from pathlib import Path
from typing import Self


class SelectedCounts(IntFlag):
    NONE = 0
    LINES = auto()
    WORDS = auto()
    CHARS = auto()
    BYTES = auto()

    @classmethod
    def default(cls: type[Self]) -> Self:
        return cls.LINES | cls.WORDS | cls.BYTES


class Arguments(Namespace):
    @cached_property
    def selected_counts(self) -> SelectedCounts:
        selected = self.lines | self.words | self.chars | self.bytes
        return selected or SelectedCounts.default()


@dataclass
class Counts:
    lines: int = 0
    words: int = 0
    bytes: int = 0
    chars: int = 0

    def __add__(self, other: type[Self]) -> Self:
        return Counts(
            lines=self.lines + other.lines,
            words=self.words + other.words,
            bytes=self.bytes + other.bytes,
            chars=self.chars + other.chars,
        )

    def numbers(self, selected_counts: SelectedCounts) -> list[int]:
        return [
            getattr(self, flag.name.lower())
            for flag in SelectedCounts
            if flag & selected_counts
        ]

    def max_digits(self, selected_counts: SelectedCounts) -> int:
        return len(str(max(self.numbers(selected_counts))))

    def to_string(
        self, selected_counts: SelectedCounts, max_digits: int
    ) -> str:
        return " ".join(
            f"{number:>{max_digits}}"
            for number in self.numbers(selected_counts)
        )


@dataclass(frozen=True)
class FileStats:
    path: Path
    counts: Counts

    @classmethod
    def from_path(cls: type[Self], path: Path) -> Self:
        if path == Path("-"):
            raw_content = sys.stdin.buffer.read()
        elif path.is_file():
            raw_content = path.read_bytes()
        else:
            return cls(path, Counts())
        content = raw_content.decode("utf-8")
        return cls(
            path,
            Counts(
                lines=content.count("\n"),
                words=len(re.findall(r"\w+", content)),
                bytes=len(raw_content),
                chars=len(content),
            ),
        )


def main() -> None:
    args = parse_args()
    if len(args.paths) > 0:
        files_counts = [FileStats.from_path(path) for path in args.paths]
    else:
        files_counts = [FileStats.from_path(Path("-"))]
    display(files_counts, args.selected_counts)


def parse_args() -> Arguments:
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


def display(
    files_counts: list[FileStats], selected_counts: SelectedCounts
) -> None:
    total_counts = sum((file.counts for file in files_counts), Counts())
    max_digits = total_counts.max_digits(selected_counts)
    for file in files_counts:
        line = file.counts.to_string(selected_counts, max_digits)
        if file.path == Path("-"):
            print(line)
        elif not file.path.exists():
            print(line, file.path, "(no such file or directory)")
        elif file.path.is_dir():
            print(line, f"{file.path}/ (is a directory)")
        else:
            print(line, file.path)
    if len(files_counts) > 1:
        print(total_counts.to_string(selected_counts, max_digits), "total")
