from subprocess import run

from realpython import task


@task(
    number=6,
    name="Handle Directories and Missing Files",
    url="TODO",
)
class Test:
    def test_reports_a_missing_file(self, random_filename):
        process = run(["wordcount", random_filename], capture_output=True)
        assert process.stdout == f"0 0 0 {random_filename} (no such file or directory)\n".encode()

    def test_reports_a_directory(self, fake_dir):
        process = run(["wordcount", fake_dir], capture_output=True)
        assert process.stdout == f"0 0 0 {fake_dir}/ (is a directory)\n".encode()
