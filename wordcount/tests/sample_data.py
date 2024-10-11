"""
TODO Generators

TODO Now, it makes senset to show expected vs actual with assert_special()

def short_word(with_newline: bool):
    ...

def compound_word():
    ...

def with_newline(newline: Literal["\n", "\r", "\r\n"]):
    ...
"""
import random
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from string import ascii_lowercase
from tempfile import gettempdir

import pytest

# Task 02 / Task 05
stdin_short_word = [
    (b"caffe", b"0 1 5\n"),         # No trailing newline
    (b"caffe\n", b"1 1 6\n"),       # With trailing newline
    (b"back-end\n", b"1 1 9\n"),    # Delimit on whitespace, special characters
    (b"hot\ntea", b"1 2 7\n"),      # Linux newline
    (b"hot\rtea", b"0 2 7\n"),      # macOS newline
    (b"hot\r\ntea", b"1 2 8\n"),    # Windows newline
    (b"latte\n", b"1 1 6\n"),       # Task 05 (wordcount -) dash character
]

# Task 03
stdin_short_word_with_unicode = [
    (b"caff\xc3\xa8", b"0 1 6\n"),   # Unicode multi-byte characters
    (b"caff\xc3\xa8\n", b"1 1 7\n"),  # With trailing newline
]

# Task 04
stdin_long_word = [
    (b"floccinaucinihilipilification", b" 0  1 29\n"),
    (b"floccinaucinihilipilification\n", b" 1  1 30\n")  # With trailing newline
]

stdin_multiple_words = [
    (b"Lorem ipsum dolor sit amet", b" 0  5 26\n"),
    (b"Lorem ipsum dolor sit amet\n", b" 1  5 27\n"),  # With newline
]

stdin_multiple_lines = [
    (
        (
            b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\n"
            b"tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\n"
            b"quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\n"
            b"consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\n"
            b"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\n"
            b"proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
        ),
        b"  6  69 447\n"
    ),
]

# --------------------------------------------------------------------------------

@dataclass
class FakeFile:
    content: bytes
    counts: tuple[int, ...]

    @cached_property
    def path(self) -> Path:
        name = "".join(random.choices(ascii_lowercase, k=10))
        return Path(gettempdir()) / name

    def create(self):
        self.path.write_bytes(self.content)

    # def format_line(self, max_digits, selected_counts):
    def format_line(self):
        return f" 1  2 12 {self.path}".encode("utf-8")
        # return " ".join(
        #     f"{number:>{max_digits}}"
        #     for number in self.numbers(selected_counts)
        # )

    def delete(self):
        if self.path.is_dir():
            self.path.rmdir()
        elif self.path.is_file():
            self.path.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def file1():
    fake_file = random.choice([
        FakeFile(
            content=b"Mocha",
            counts=(0, 1, 5, 5)
        ),
        FakeFile(
            content=b"Espresso\n",
            counts=(1, 1, 9, 9)
        ),
        FakeFile(
            content=b"Cappuccino\n",
            counts=(1, 1, 11, 11)
        ),
        FakeFile(
            content=b"Frappuccino",
            counts=(0, 1, 11, 11)
        ),
        FakeFile(
            content=b"Flat White\n",
            counts=(1, 2, 11, 11)
        ),
        FakeFile(
            content=b"Turkish Coffee",
            counts=(0, 2, 14, 14)
        ),
        FakeFile(
            content=b"Irish Coffee Drink\n",
            counts=(1, 3, 19, 19)
        ),
        FakeFile(
            content=b"Espresso con Panna",
            counts=(0, 3, 18, 18)
        ),
    ])
    try:
        fake_file.create()
        yield fake_file
    finally:
        fake_file.delete()





# Task 05
file_simple = [
    (b"caffe latte\n", " 1  2 12 {path}\n".encode()),
]

# Task 06
special_cases = [
    ("fake_dir/", "0 0 0 {fake_dir}/ (is a directory)\n".encode()),
    ("random_filename", "0 0 0 {random_filename} (no such file or directory)\n".encode()),
]

# Task 07
multiple_files = [
    (b"caffe latte\n", " 1  2 12 {path1}\n".encode()),
    (b"Lorem ipsum dolor sit amet\n", " 1  5 27 {path2}\n".encode()),
    ("Zażółć gęślą jaźń\n".encode("utf-8"), " 1  3 27 {path3}\n".encode()),
    (..., b" 3 10 66 total\n")  # Totals

    # 3x caffe latte (the same file) and the corresponding totals
]

files_and_stdin = [
    (b"Lorem ipsum dolor sit amet\n", " 1  5 27 {path}\n"),
    (b"caffe latte", " 0  2 11\n"),
    (..., " 1  7 38 total\n"),  # Totals

    # f"0 0 0 {fake_dir}/ (is a directory)\n".encode(),
    # f"0 0 0 {random_filename} (no such file or directory)\n".encode(),
    # b"0 0 0 total\n"
]
