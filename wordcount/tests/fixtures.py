from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest


@pytest.fixture
def temporary_path():
    with NamedTemporaryFile(mode="wb", delete=False) as file:
        file.write(b"caffe latte\n")
        path = Path(file.name)
    try:
        yield path
    finally:
        file.close()
        path.unlink(missing_ok=True)


@pytest.fixture
def temporary_dir():
    with TemporaryDirectory(delete=False) as directory:
        path = Path(directory)
    try:
        yield path
    finally:
        path.rmdir()


# TODO doesn't clean up after itself, maybe make a global register
@pytest.fixture
def temporary_path_factory():
    def temporary_path(content):
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as file:
            file.write(content)
            return Path(file.name)

    return temporary_path
