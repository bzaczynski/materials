from subprocess import run

from realpython import task


@task(
    number=5,
    name="Read Data From a File",
    url="TODO",
)
class Test:
    def test_displays_counts_and_a_filename_on_the_same_line(self, temporary_path):
        process = run(["wordcount", str(temporary_path)], capture_output=True)
        assert process.stdout == f" 1  2 12 {temporary_path}\n".encode()

    def test_treats_the_dash_character_as_standard_input(self):
        process = run(["wordcount", "-"], capture_output=True, input=b"latte\n")
        assert process.stdout == b"1 1 6\n"
