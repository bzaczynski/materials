from itertools import permutations
from subprocess import run

from realpython import task


@task(
    number=9,
    name="Select Counts With Command-Line Options",
    url="TODO",
)
class Test:
    def test_counts_lines_words_bytes_in_stdin_by_default(self):
        """Counts lines, words, and bytes in stdin by default"""
        command = ["wordcount"]
        process = run(command, capture_output=True, input=b"caffe\nlatte\nflat white\n")
        assert process.stdout == b" 3  4 23\n"

    def test_counts_lines_words_bytes_in_stdin_explicitly(self, make_file, fake_dir, random_filename):
        """Counts lines, words, and bytes in stdin explicitly"""
        command = ["wordcount", "--lines", "--words", "--bytes"]
        process = run(command, capture_output=True, input=b"caffe\nlatte\nflat white\n")
        assert process.stdout == b" 3  4 23\n"

    def test_only_counts_lines_in_stdin(self, make_file, fake_dir, random_filename):
        command = ["wordcount", "--lines"]
        process = run(command, capture_output=True, input=b"caffe\nlatte\nflat white\n")
        assert process.stdout == b"3\n"

    def test_only_counts_words_in_stdin(self, make_file, fake_dir, random_filename):
        command = ["wordcount", "--words"]
        process = run(command, capture_output=True, input=b"caffe\nlatte\nflat white\n")
        assert process.stdout == b"4\n"

    def test_only_counts_bytes_in_stdin(self, make_file, fake_dir, random_filename):
        command = ["wordcount", "--bytes"]
        process = run(command, capture_output=True, input=b"caffe\nlatte\nflat white\n")
        assert process.stdout == b"23\n"

    def test_counts_lines_and_words_in_stdin(self, make_file, fake_dir, random_filename):
        command = ["wordcount", "--lines", "--words"]
        process = run(command, capture_output=True, input=b"caffe\nlatte\nflat white\n")
        assert process.stdout == b"3 4\n"

    def test_counts_lines_and_bytes_in_stdin(self, make_file, fake_dir, random_filename):
        command = ["wordcount", "--lines", "--bytes"]
        process = run(command, capture_output=True, input=b"caffe\nlatte\nflat white\n")
        assert process.stdout == b" 3 23\n"

    def test_counts_words_and_bytes_in_stdin(self, make_file, fake_dir, random_filename):
        command = ["wordcount", "--words", "--bytes"]
        process = run(command, capture_output=True, input=b"caffe\nlatte\nflat white\n")
        assert process.stdout == b" 4 23\n"

    def test_always_displays_counts_of_stdin_in_the_same_order(self, make_file, fake_dir, random_filename):
        for flags in permutations(["--lines", "--words", "--bytes"]):
            command = ["wordcount", *flags]
            process = run(command, capture_output=True, input=b"caffe\nlatte\nflat white\n")
            assert process.stdout == b" 3  4 23\n"

    def test_counts_lines_words_bytes_by_default(self, make_file, fake_dir, random_filename):
        """Counts lines, words, and bytes by default"""
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
                f"  1   1   6 {path1}\n".encode(),
                b"  0   2  10\n",
                f"  1   3  27 {path2}\n".encode(),
                f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0   0\n",
                f"  6  69 447 {path3}\n".encode(),
                f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                b"  8  75 490 total\n",
            ])
            command = ["wordcount", path1, "-", path2, fake_dir, "-", path3, random_filename]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_counts_lines_words_bytes_explicitly(self, make_file, fake_dir, random_filename):
        """Counts lines, words, and bytes explicitly"""
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
                f"  1   1   6 {path1}\n".encode(),
                b"  0   2  10\n",
                f"  1   3  27 {path2}\n".encode(),
                f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0   0\n",
                f"  6  69 447 {path3}\n".encode(),
                f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                b"  8  75 490 total\n",
            ])
            command = [
                "wordcount", "--lines", "--words", "--bytes",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_only_counts_lines(self, make_file, fake_dir, random_filename):
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
                f"1 {path1}\n".encode(),
                b"0\n",
                f"1 {path2}\n".encode(),
                f"0 {fake_dir}/ (is a directory)\n".encode(),
                b"0\n",
                f"6 {path3}\n".encode(),
                f"0 {random_filename} (no such file or directory)\n".encode(),
                b"8 total\n",
            ])
            command = [
                "wordcount", "--lines",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_only_counts_words(self, make_file, fake_dir, random_filename):
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
                f" 1 {path1}\n".encode(),
                b" 2\n",
                f" 3 {path2}\n".encode(),
                f" 0 {fake_dir}/ (is a directory)\n".encode(),
                b" 0\n",
                f"69 {path3}\n".encode(),
                f" 0 {random_filename} (no such file or directory)\n".encode(),
                b"75 total\n",
            ])
            command = [
                "wordcount", "--words",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_only_counts_bytes(self, make_file, fake_dir, random_filename):
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
                f"  6 {path1}\n".encode(),
                b" 10\n",
                f" 27 {path2}\n".encode(),
                f"  0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0\n",
                f"447 {path3}\n".encode(),
                f"  0 {random_filename} (no such file or directory)\n".encode(),
                b"490 total\n",
            ])
            command = [
                "wordcount", "--bytes",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_counts_lines_and_words(self, make_file, fake_dir, random_filename):
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
                f" 1  1 {path1}\n".encode(),
                b" 0  2\n",
                f" 1  3 {path2}\n".encode(),
                f" 0  0 {fake_dir}/ (is a directory)\n".encode(),
                b" 0  0\n",
                f" 6 69 {path3}\n".encode(),
                f" 0  0 {random_filename} (no such file or directory)\n".encode(),
                b" 8 75 total\n",
            ])
            command = [
                "wordcount", "--lines", "--words",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_counts_lines_and_bytes(self, make_file, fake_dir, random_filename):
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
                f"  1   6 {path1}\n".encode(),
                b"  0  10\n",
                f"  1  27 {path2}\n".encode(),
                f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0\n",
                f"  6 447 {path3}\n".encode(),
                f"  0   0 {random_filename} (no such file or directory)\n".encode(),
                b"  8 490 total\n",
            ])
            command = [
                "wordcount", "--lines", "--bytes",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_counts_words_and_bytes(self, make_file, fake_dir, random_filename):
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
                f"  1   6 {path1}\n".encode(),
                b"  2  10\n",
                f"  3  27 {path2}\n".encode(),
                f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0\n",
                f" 69 447 {path3}\n".encode(),
                f"  0   0 {random_filename} (no such file or directory)\n".encode(),
                b" 75 490 total\n",
            ])
            command = [
                "wordcount", "--words", "--bytes",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_always_displays_counts_in_the_same_order(self, make_file, fake_dir, random_filename):    #
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
                f"  1   1   6 {path1}\n".encode(),
                b"  0   2  10\n",
                f"  1   3  27 {path2}\n".encode(),
                f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0   0\n",
                f"  6  69 447 {path3}\n".encode(),
                f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                b"  8  75 490 total\n",
            ])
            for flags in permutations(["--lines", "--words", "--bytes"]):
                command = [
                    "wordcount", *flags,
                    path1, "-", path2, fake_dir, "-", path3, random_filename
                ]
                process = run(command, capture_output=True, input=b"flat white")
                assert process.stdout == expected
