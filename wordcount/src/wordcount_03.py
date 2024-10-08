import sys


def main():
    raw_text = sys.stdin.buffer.read()
    text = raw_text.decode("utf-8")
    num_lines = text.count("\n")
    num_words = len(text.split())
    num_bytes = len(raw_text)
    print(num_lines, num_words, num_bytes)
