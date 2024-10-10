import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Counts:
    lines: int = 0
    words: int = 0
    bytes: int = 0


@dataclass
class FileStats:
    path: Path
    counts: Counts

    @classmethod
    def from_path(cls, path):
        if path == Path("-"):
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
    if sys.argv[1:]:
        paths = [Path(arg) for arg in sys.argv[1:]]
    else:
        paths = [Path("-")]

    files_stats = [FileStats.from_path(p) for p in paths]


    # total_counts = (0, 0, 0)
    # max_digits = len(str(max(total_counts)))

    # ----------------------

    # if paths := [Path(arg) for arg in sys.argv[1:]]:
    #     files_counts
    #     total_counts = (0, 0, 0)
    #     max_digits = 0
    #     for path in paths:
    #         if path.name == "-":
    #             total_counts = add(total_counts, read_stdin())
    #         elif not path.exists():
    #             print(f"0 0 0 {path} (no such file or directory)")
    #         elif path.is_dir():
    #             print(f"0 0 0 {path}/ (is a directory)")
    #         else:
    #             total_counts = add(total_counts, read_file(path))
    #     if len(paths) > 1:
    #         print(to_string(*total_counts), "total")
    # else:
    #     read_stdin()

#
# # def add(total_counts, counts):
# #     return tuple(a + b for a, b in zip(total_counts, counts))
# #
# #
# # def read_stdin():
# #     counts = get_counts(sys.stdin.buffer.read())
# #     print(to_string(*counts))
# #     return counts
# #
# #
# # def read_file(path):
# #     counts = get_counts(path.read_bytes())
# #     print(to_string(*counts), path)
# #     return counts
# #
# #
# # def get_counts(raw_text):
# #     text = raw_text.decode("utf-8")
# #     num_lines = text.count("\n")
# #     num_words = len(text.split())
# #     num_bytes = len(raw_text)
# #     return num_lines, num_words, num_bytes
# #
# #
# # def to_string(num_lines, num_words, num_bytes):
# #     max_digits = len(str(max(num_lines, num_words, num_bytes)))
# #     return (
# #         f"{num_lines:>{max_digits}} "
# #         f"{num_words:>{max_digits}} "
# #         f"{num_bytes:>{max_digits}}"
# #     )
