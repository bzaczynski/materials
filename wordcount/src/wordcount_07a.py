"""
Read data from multiple files.
"""

import sys
from pathlib import Path


def main():
    if len(sys.argv) > 1:
        paths = [Path(arg) for arg in sys.argv[1:]]
    else:
        paths = [Path("-")]
    for path in paths:
        try:
            if path.name == "-":
                raw_text = sys.stdin.buffer.read()
            else:
                raw_text = path.read_bytes()
            text = raw_text.decode("utf-8")
            num_lines = text.count("\n")
            num_words = len(text.split())
            num_bytes = len(raw_text)
            max_digits = len(str(max(num_lines, num_words, num_bytes)))
            output = (
                f"{num_lines:>{max_digits}} "
                f"{num_words:>{max_digits}} "
                f"{num_bytes:>{max_digits}}"
            )
            if path.name != "-":
                print(output, path)
            else:
                print(output)
        except IsADirectoryError:
            print(f"0 0 0 {path}/ (is a directory)")
        except FileNotFoundError:
            print(f"0 0 0 {path} (no such file or directory)")
