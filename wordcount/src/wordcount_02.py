"""
# First attempt (doesn't use the expected formatting):

import sys

def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
    num_words = len(text.split())
    num_bytes = len(text)
    print(num_lines, num_words, num_bytes)
"""

import sys

def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
    num_words = len(text.split())
    num_bytes = len(text)
    max_digits = len(str(max(num_lines, num_words, num_bytes)))
    print(
        f"{num_lines:>{max_digits}} "
        f"{num_words:>{max_digits}} "
        f"{num_bytes:>{max_digits}}"
    )
