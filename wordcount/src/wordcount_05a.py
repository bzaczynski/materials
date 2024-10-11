"""
Add the ability to read from a file using sys.argv[1].

Note that you get the second acceptance criteria successful for free now,
but only until using sys.argv.
"""

import sys
from pathlib import Path


def main():
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        raw_text = path.read_bytes()
    else:
        path = None
        raw_text = sys.stdin.buffer.read()
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
    if path:
        print(output, path)
    else:
        print(output)
