import random
import string
from string import ascii_lowercase
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory, gettempdir

import pytest

# --------------------------------------------------------------

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
        return f" 1  2 12 {self.path}\n".encode("utf-8")
        # TODO
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




# --------------------------------------------------------------

@pytest.fixture(scope="session")
def wc():
    def function(*args, stdin: bytes | None = None) -> bytes:
        process = run(["wordcount", *args], capture_output=True, input=stdin)
        return process.stdout

    return function


@pytest.fixture(scope="session")
def fake_dir():
    with TemporaryDirectory(delete=False) as directory:
        path = Path(directory)
        try:
            yield path
        finally:
            path.rmdir()


# TODO file1, file2, file3 fixture
# Should probably draw at random at first and then reuse?

@pytest.fixture
def make_file():
    @contextmanager
    def factory(content: str | bytes, name: str | None = None) -> Path:
        path = Path(gettempdir()) / (name or make_random_filename())
        if isinstance(content, str):
            path.write_text(content, encoding="utf-8")
        else:
            path.write_bytes(content)
        try:
            yield path
        finally:
            path.unlink(missing_ok=True)

    return factory


@pytest.fixture(scope="function")
def random_filename():
    return make_random_filename()


def make_random_filename(length=10) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))
