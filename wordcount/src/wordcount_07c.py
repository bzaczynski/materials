import sys
from pathlib import Path


def main():
    if sys.argv[1:]:
        paths = [Path(arg) for arg in sys.argv[1:]]
    else:
        paths = [Path("-")]
    total_counts = (0, 0, 0)
    files_stats = []
    for path in paths:
        if path.name == "-":
            counts = get_counts(sys.stdin.buffer.read())
            total_counts = add(total_counts, counts)
        elif not path.exists() or path.is_dir():
            counts = (0, 0, 0)
        else:
            counts = get_counts(path.read_bytes())
            total_counts = add(total_counts, counts)
        files_stats.append((path, counts))
    max_digits = len(str(max(max(stats[1]) for stats in files_stats)))
    for path, counts in files_stats:
        if path.name == "-":
            print(to_string(*counts, max_digits))
        elif not path.exists():
            print(f"{to_string(*counts, max_digits)} {path} (no such file or directory)")
        elif path.is_dir():
            print(f"{to_string(*counts, max_digits)} {path}/ (is a directory)")
        else:
            print(to_string(*counts, max_digits), path)
    if len(paths) > 1:
        print(to_string(*total_counts, max_digits), "total")


def get_counts(raw_text):
    text = raw_text.decode("utf-8")
    num_lines = text.count("\n")
    num_words = len(text.split())
    num_bytes = len(raw_text)
    return num_lines, num_words, num_bytes


def to_string(num_lines, num_words, num_bytes, max_digits):
    return (
        f"{num_lines:>{max_digits}} "
        f"{num_words:>{max_digits}} "
        f"{num_bytes:>{max_digits}}"
    )


def add(total_counts, counts):
    return tuple(a + b for a, b in zip(total_counts, counts))
