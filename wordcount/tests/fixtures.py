import random
import string
from contextlib import contextmanager
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory, gettempdir

import pytest


@pytest.fixture
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


@pytest.fixture(scope="session")
def random_filename():
    return make_random_filename()


def make_random_filename(length=10) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))
