"""
Format the numbers according to the maximum number of digits in the counts.
"""

import sys


def main():
    raw_text = sys.stdin.buffer.read()
    text = raw_text.decode("utf-8")
    num_lines = text.count("\n")
    num_words = len(text.split())
    num_bytes = len(raw_text)
    max_digits = len(str(max(num_lines, num_words, num_bytes)))
    print(
        f"{num_lines:>{max_digits}} "
        f"{num_words:>{max_digits}} "
        f"{num_bytes:>{max_digits}}"
    )
