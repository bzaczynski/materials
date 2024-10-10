from subprocess import run

from realpython import task


@task(
    number=7,
    name="Read Data From Multiple Files",
    url="TODO",
)
class Test:
    def test_displays_counts_and_filenames_on_separate_lines(self, make_file):
        with (
            make_file(b"caffe latte\n") as path1,
            make_file(b"Lorem ipsum dolor sit amet\n") as path2,
            make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path3,
        ):
            expected = b"".join([
                f" 1  2 12 {path1}\n".encode(),
                f" 1  5 27 {path2}\n".encode(),
                f" 1  3 27 {path3}\n".encode(),
            ])
            process = run(["wordcount", path1, path2, path3], capture_output=True)
            assert process.stdout.startswith(expected)

    def test_includes_a_summary_with_total_counts(self, make_file):
        with (
            make_file(b"caffe latte\n") as path1,
            make_file(b"Lorem ipsum dolor sit amet\n") as path2,
            make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path3,
        ):
            process = run(["wordcount", path1, path2, path3], capture_output=True)
            assert process.stdout.endswith(b" 3 10 66 total\n")

    def test_can_repeat_the_same_file_multiple_times(self, make_file):
        with make_file(b"caffe latte\n") as path:
            process = run(["wordcount", path, path, path], capture_output=True)
            expected = (
                f" 1  2 12 {path}\n"
                f" 1  2 12 {path}\n"
                f" 1  2 12 {path}\n"
                f" 3  6 36 total\n"
            )
            assert process.stdout == expected.encode()

    def test_can_mix_files_with_standard_input(self, make_file):
        with make_file(b"Lorem ipsum dolor sit amet\n") as path:
            command = ["wordcount", path, "-"]
            process = run(command, capture_output=True, input=b"caffe latte")
            expected = f" 1  5 27 {path}\n 0  2 11\n 1  7 38 total\n"
            assert process.stdout == expected.encode()

    # @pytest.mark.skip
    # def test_can_repeat_standard_input_multiple_times(self, make_file):
    #     pass

    def test_reports_a_directory_and_a_missing_file(self, random_filename, fake_dir):
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
