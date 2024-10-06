from subprocess import run

from realpython import task


@task(
    number=2,
    name="Read Data from Standard Input",
    url="TODO",
)
class Test:
    def test_read_bytes_from_stdin(self):
        process = run(["wordcount"], capture_output=True)
        assert process.returncode == 0
