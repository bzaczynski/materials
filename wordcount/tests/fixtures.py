import random
import string

from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory, gettempdir

import pytest

# TODO session-scoped fixtures with files that will be removed afterwards?


@pytest.fixture
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


@pytest.fixture
def random_filename():
    return make_random_filename()


def make_random_filename(length=10) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))
