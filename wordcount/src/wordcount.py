"""
Add a rudimentary implementation that reads data from stdin and prints the counts.
"""

import sys


def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
    num_words = len(text.split())
    num_bytes = len(text)
    print(num_lines, num_words, num_bytes)
