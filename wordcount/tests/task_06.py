import random
import string
from subprocess import run

from realpython import task


@task(
    number=6,
    name="Handle Directories and Missing Files",
    url="TODO",
)
class Test:
    def test_reports_a_missing_file(self):
        random_filename = "".join(random.choices(string.ascii_letters, k=10))
        process = run(["wordcount", random_filename], capture_output=True)
        assert process.stdout == f"0 0 0 {random_filename} (no such file or directory)\n".encode()

    def test_reports_a_directory(self, temporary_dir):
        process = run(["wordcount", temporary_dir], capture_output=True)
        assert process.stdout == f"0 0 0 {temporary_dir}/ (is a directory)\n".encode()
