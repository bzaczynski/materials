import sys
from pathlib import Path


def main():
    if paths := [Path(arg) for arg in sys.argv[1:]]:
        for path in paths:
            if path.name == "-":
                read_stdin()
            elif not path.exists():
                print(f"0 0 0 {path} (no such file or directory)")
            elif path.is_dir():
                print(f"0 0 0 {path}/ (is a directory)")
            else:
                read_file(path)
    else:
        read_stdin()


def read_stdin():
    output = to_string(*get_counts(sys.stdin.buffer.read()))
    print(output)


def read_file(path):
    output = to_string(*get_counts(path.read_bytes()))
    print(output, path)


def get_counts(raw_text):
    text = raw_text.decode("utf-8")
    num_lines = text.count("\n")
    num_words = len(text.split())
    num_bytes = len(raw_text)
    return num_lines, num_words, num_bytes


def to_string(num_lines, num_words, num_bytes):
    max_digits = len(str(max(num_lines, num_words, num_bytes)))
    return (
        f"{num_lines:>{max_digits}} "
        f"{num_words:>{max_digits}} "
        f"{num_bytes:>{max_digits}}"
    )