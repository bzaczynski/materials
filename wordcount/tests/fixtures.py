import random
import string
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from itertools import permutations
from pathlib import Path
from string import ascii_lowercase
from subprocess import run
from tempfile import TemporaryDirectory, gettempdir

import pytest


@dataclass
class FakeFile:
    content: bytes
    counts: tuple[int, ...]

    def __post_init__(self):
        self.path.write_bytes(self.content)

    @cached_property
    def path(self) -> Path:
        name = "".join(random.choices(ascii_lowercase, k=10))
        return Path(gettempdir()) / name

    # def format_line(self, max_digits, selected_counts):
    def format_line(self):
        md = len(str(max(self.counts)))
        return f"{self.counts[0]:{md}} {self.counts[1]:{md}} {self.counts[3]:{md}} {self.path}\n".encode("utf-8")
        # TODO
        # TODO bitwise operators
        # return " ".join(
        #     f"{number:>{max_digits}}"
        #     for number in self.numbers(selected_counts)
        # )

    def delete(self):
        if self.path.is_dir():
            self.path.rmdir()
        elif self.path.is_file():
            self.path.unlink(missing_ok=True)


@dataclass(frozen=True)
class Files:
    files: list[FakeFile]

    def __iter__(self):
        return iter(self.files)

    def __len__(self):
        return len(self.files)

    @cached_property
    def paths(self):
        return [str(file.path) for file in self.files]

    @cached_property
    def expected(self):
        return b""  # TODO


@pytest.fixture(scope="session")
def small_file():
    fake_file = FakeFile(
        content=b"caffe\n",
        counts=(1, 1, 6, 6)
    )
    try:
        yield fake_file
    finally:
        fake_file.delete()


@pytest.fixture(scope="session")
def file1():
    fake_file = FakeFile(
        content=b"caffe latte\n",
        counts=(1, 2, 12, 12)
    )
    try:
        yield fake_file
    finally:
        fake_file.delete()


@pytest.fixture(scope="session")
def file2():
    fake_file = FakeFile(
        content=b"Lorem ipsum dolor sit amet\n",
        counts=(1, 5, 27, 27)
    )
    try:
        yield fake_file
    finally:
        fake_file.delete()


@pytest.fixture(scope="session")
def file3():
    fake_file = FakeFile(
        content="Zażółć gęślą jaźń\n".encode("utf-8"),
        counts=(1, 3, 18, 27)
    )
    try:
        yield fake_file
    finally:
        fake_file.delete()



@pytest.fixture(scope="session")
def small_files():
    fake_files = [
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
    ]
    try:
        yield Files(fake_files)
    finally:
        for file in fake_files:
            file.delete()


@pytest.fixture(scope="session")
def medium_files(file1, file2, file3):
    return Files([file1, file2, file3])


@pytest.fixture(scope="session")
def file_batches(medium_files):
    return [
        batch
        for length in range(1, len(medium_files) + 1)
        for batch in permutations(medium_files, length)
    ]


# @pytest.fixture(scope="session")
# def file1():
#     fake_file = random.choice([
#         FakeFile(
#             content=b"Mocha",
#             counts=(0, 1, 5, 5)
#         ),
#         FakeFile(
#             content=b"Espresso\n",
#             counts=(1, 1, 9, 9)
#         ),
#         FakeFile(
#             content=b"Cappuccino\n",
#             counts=(1, 1, 11, 11)
#         ),
#         FakeFile(
#             content=b"Frappuccino",
#             counts=(0, 1, 11, 11)
#         ),
#         FakeFile(
#             content=b"Flat White\n",
#             counts=(1, 2, 11, 11)
#         ),
#         FakeFile(
#             content=b"Turkish Coffee",
#             counts=(0, 2, 14, 14)
#         ),
#         FakeFile(
#             content=b"Irish Coffee Drink\n",
#             counts=(1, 3, 19, 19)
#         ),
#         FakeFile(
#             content=b"Espresso con Panna",
#             counts=(0, 3, 18, 18)
#         ),
#     ])
#     try:
#         fake_file.create()
#         yield fake_file
#     finally:
#         fake_file.delete()


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


@pytest.fixture
def make_file():
    @contextmanager
    def factory(content: str | bytes, name: str | None = None) -> Path:
        path = Path(gettempdir()) / (name or make_random_name())
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
def random_name():
    return make_random_name()


def make_random_name(length=10) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))
