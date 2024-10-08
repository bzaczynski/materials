import tempfile
from pathlib import Path
from subprocess import run

import pytest

from realpython import task


@pytest.fixture
def temporary_path():
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as file:
        file.write(b"caffe latte\n")
        path = Path(file.name)
    try:
        yield path
    finally:
        file.close()
        path.unlink(missing_ok=True)


@task(
    number=5,
    name="Read Data From a File",
    url="TODO",
)
class Test:
    def test_display_counts_and_a_filename_on_the_same_line(self, temporary_path):
        process = run(["wordcount", str(temporary_path)], capture_output=True)
        assert process.stdout == f" 1  2 12 {temporary_path}\n".encode()

    def test_treat_the_dash_character_as_standard_input(self):
        process = run(["wordcount", "-"], capture_output=True, input=b"latte\n")
        assert process.stdout == b"1 1 6\n"
