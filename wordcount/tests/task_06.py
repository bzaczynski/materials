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

    def test_reports_both(self, random_filename, fake_dir):
        process = run(["wordcount", fake_dir, random_filename], capture_output=True)
        assert process.stdout == b"".join([
            f"0 0 0 {fake_dir}/ (is a directory)\n".encode(),
            f"0 0 0 {random_filename} (no such file or directory)\n".encode(),
            b"0 0 0 total\n"
        ])

    def test_reports_a_mix_of_all(self, random_filename, fake_dir, make_file):
        with make_file(b"caffe\n") as path:
            command = ["wordcount", fake_dir, str(path), random_filename, "-"]
            process = run(command, capture_output=True, input=b"hot")
            assert process.stdout == b"".join([
                f"0 0 0 {fake_dir}/ (is a directory)\n".encode(),
                f"1 1 6 {path}\n".encode(),
                f"0 0 0 {random_filename} (no such file or directory)\n".encode(),
                b"0 1 3\n",
                b"1 2 9 total\n"
            ])
