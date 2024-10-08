from subprocess import run

import pytest

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

    def test_repeats_the_same_file_multiple_times(self, make_file):
        with make_file(b"caffe latte\n") as path:
            process = run(["wordcount", path, path, path], capture_output=True)
            expected = (
                f" 1  2 12 {path}\n"
                f" 1  2 12 {path}\n"
                f" 1  2 12 {path}\n"
                f" 3  6 36 total\n"
            )
            assert process.stdout == expected.encode()

    @pytest.mark.skip
    def test_repeats_standard_input_multiple_times(self, make_file):
        pass

    def test_mixes_files_with_standard_input(self, make_file):
        with make_file(b"Lorem ipsum dolor sit amet\n") as path:
            command = ["wordcount", path, "-"]
            process = run(command, capture_output=True, input=b"caffe latte")
            expected = f" 1  5 27 {path}\n 0  2 11\n 1  7 38 total\n"
            assert process.stdout == expected.encode()

    def test_uses_consistent_formatting_across_lines(self, make_file, fake_dir, random_filename):
        with (
            make_file(b"short\n") as path1,
            make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path2,
            make_file(
                b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\n"
                b"tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\n"
                b"quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\n"
                b"consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\n"
                b"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\n"
                b"proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
            ) as path3,
        ):
            expected = b"".join([
                f"  1   1   6 {path1}".encode(),
                b"  0   2  10",
                f"  1   3  27 {path2}".encode(),
                f"  0   0   0 {fake_dir} (is a directory)".encode(),
                b"  0   0   0",
                f"  6  69 447 {path3}".encode(),
                f"  0   0   0 {random_filename} (no such file or directory)".encode(),
                b"  8  75 490 total",
            ])
            command = ["wordcount", path1, "-", path2, fake_dir, "-", path3, random_filename]
            process = run(command, capture_output=True, input=b"flat white")
            print(process.stdout.decode())
            assert process.stdout == expected


    #     with (
    #         make_file(b"Lorem ipsum dolor sit amet\n") as path1,
    #         make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path2,
    #     ):
    #
    #         stdin_copy = os.fdopen(os.dup(sys.stdin.fileno()), sys.stdin.mode)
    #
    #         command = ["wordcount", "-", path1, "-", path2]
    #         process = Popen(command, stdin=PIPE, stdout=PIPE)
    #         process.stdin.write(b"caffe latte\n")
    #         process.stdin.close()
    #
    #         process.stdin = stdin_copy
    #         process.stdin.write(b"hot tea\n")

    # TODO Next up: argparse
    # TODO Next up: counts selection
    # TODO Next up: formatting advanced?
