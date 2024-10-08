import random
import string
import tempfile
from pathlib import Path
from subprocess import run

import pytest

from realpython import task


@pytest.fixture
def temporary_dir():
    with tempfile.TemporaryDirectory(delete=False) as directory:
        path = Path(directory)
    try:
        yield path
    finally:
        path.rmdir()


@task(
    number=6,
    name="Handle Directories and Missing Files",
    url="TODO",
)
class Test:
    def test_indicate_missing_file(self):
        random_filename = "".join(random.choices(string.ascii_letters, k=10))
        process = run(["wordcount", random_filename], capture_output=True)
        assert process.stdout == f"0 0 0 {random_filename} (no such file or directory)\n".encode()

    def test_indicate_directory(self, temporary_dir):
        process = run(["wordcount", temporary_dir], capture_output=True)
        assert process.stdout == f"0 0 0 {temporary_dir}/ (is a directory)\n".encode()


    # TODO relative vs absolute path

    # TODO multiple files + totals
    # TODO formatting advanced?
