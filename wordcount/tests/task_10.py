from itertools import permutations
from subprocess import run

import pytest

from realpython import task
from realpython import TEST_TIMEOUT_SECONDS


@task(
    number=10,
    name="Add Support for Counting the Characters",
    url="TODO",
)
class Test:
    def test_only_counts_characters_in_stdin(self):
        command = ["wordcount", "--chars"]
        process = run(command, capture_output=True, input="zażółć\ngęślą\njaźń\n".encode("utf-8"))
        assert process.stdout == b"18\n"

    def test_counts_characters_and_bytes_in_stdin(self):
        command = ["wordcount", "--chars", "--bytes"]
        process = run(command, capture_output=True, input="zażółć\ngęślą jaźń\n".encode("utf-8"))
        assert process.stdout == b"18 27\n"

    def test_counts_words_and_characters_in_stdin(self):
        command = ["wordcount", "--words", "--chars"]
        process = run(command, capture_output=True, input="zażółć\ngęślą jaźń\n".encode("utf-8"))
        assert process.stdout == b" 3 18\n"

    def test_counts_words_characters_bytes_in_stdin(self):
        """Counts words, characters, and bytes in stdin"""
        command = ["wordcount", "--words", "--chars", "--bytes"]
        process = run(command, capture_output=True, input="zażółć\ngęślą jaźń\n".encode("utf-8"))
        assert process.stdout == b" 3 18 27\n"

    def test_counts_lines_and_characters_in_stdin(self):
        command = ["wordcount", "--lines", "--chars"]
        process = run(command, capture_output=True, input="zażółć\ngęślą jaźń\n".encode("utf-8"))
        assert process.stdout == b" 2 18\n"

    def test_counts_lines_characters_bytes_in_stdin(self):
        """Counts lines, characters, and bytes in stdin"""
        command = ["wordcount", "--lines", "--chars", "--bytes"]
        process = run(command, capture_output=True, input="zażółć\ngęślą jaźń\n".encode("utf-8"))
        assert process.stdout == b" 2 18 27\n"

    def test_counts_lines_words_characters_in_stdin(self):
        """Counts lines, words, and characters in stdin"""
        command = ["wordcount", "--lines", "--words", "--chars"]
        process = run(command, capture_output=True, input="zażółć\ngęślą jaźń\n".encode("utf-8"))
        assert process.stdout == b" 2  3 18\n"

    def test_counts_lines_words_characters_bytes_in_stdin(self):
        """Counts lines, words, characters, and bytes in stdin"""
        command = ["wordcount", "--lines", "--words", "--chars", "--bytes"]
        process = run(command, capture_output=True, input="zażółć\ngęślą jaźń\n".encode("utf-8"))
        assert process.stdout == b" 2  3 18 27\n"

    @pytest.mark.timeout(TEST_TIMEOUT_SECONDS * 2)
    def test_always_displays_counts_of_stdin_in_the_same_order(self):
        for flags in permutations(["--lines", "--words", "--chars", "--bytes"]):
            command = ["wordcount", *flags]
            process = run(command, capture_output=True, input="zażółć\ngęślą jaźń\n".encode("utf-8"))
            assert process.stdout == b" 2  3 18 27\n"

    def test_only_counts_characters(self, make_file, fake_dir, random_filename):
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
                f" 18 {path2}\n".encode(),
                f"  0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0\n",
                f"447 {path3}\n".encode(),
                f"  0 {random_filename} (no such file or directory)\n".encode(),
                b"481 total\n",
            ])
            command = [
                "wordcount", "--chars",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_counts_characters_and_bytes(self, make_file, fake_dir, random_filename):
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
                f"  6   6 {path1}\n".encode(),
                b" 10  10\n",
                f" 18  27 {path2}\n".encode(),
                f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0\n",
                f"447 447 {path3}\n".encode(),
                f"  0   0 {random_filename} (no such file or directory)\n".encode(),
                b"481 490 total\n",
            ])
            command = [
                "wordcount", "--chars", "--bytes",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_counts_words_and_characters(self, make_file, fake_dir, random_filename):
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
                f"  3  18 {path2}\n".encode(),
                f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0\n",
                f" 69 447 {path3}\n".encode(),
                f"  0   0 {random_filename} (no such file or directory)\n".encode(),
                b" 75 481 total\n",
            ])
            command = [
                "wordcount", "--words", "--chars",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_counts_words_characters_bytes(self, make_file, fake_dir, random_filename):
        """Counts words, characters, and bytes in stdin"""
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
                f"  1   6   6 {path1}\n".encode(),
                b"  2  10  10\n",
                f"  3  18  27 {path2}\n".encode(),
                f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0   0\n",
                f" 69 447 447 {path3}\n".encode(),
                f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                b" 75 481 490 total\n",
            ])
            command = [
                "wordcount", "--words", "--chars", "--bytes",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_counts_lines_and_characters(self, make_file, fake_dir, random_filename):
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
                f"  1  18 {path2}\n".encode(),
                f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0\n",
                f"  6 447 {path3}\n".encode(),
                f"  0   0 {random_filename} (no such file or directory)\n".encode(),
                b"  8 481 total\n",
            ])
            command = [
                "wordcount", "--lines", "--chars",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_counts_lines_characters_bytes(self, make_file, fake_dir, random_filename):
        """Counts lines, characters, and bytes in stdin"""
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
                f"  1   6   6 {path1}\n".encode(),
                b"  0  10  10\n",
                f"  1  18  27 {path2}\n".encode(),
                f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0   0\n",
                f"  6 447 447 {path3}\n".encode(),
                f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                b"  8 481 490 total\n",
            ])
            command = [
                "wordcount", "--lines", "--chars", "--bytes",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_counts_lines_words_characters(self, make_file, fake_dir, random_filename):
        """Counts lines, words, and characters in stdin"""
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
                f"  1   3  18 {path2}\n".encode(),
                f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0   0\n",
                f"  6  69 447 {path3}\n".encode(),
                f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                b"  8  75 481 total\n",
            ])
            command = [
                "wordcount", "--lines", "--words", "--chars",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    def test_counts_lines_words_characters_bytes(self, make_file, fake_dir, random_filename):
        """Counts lines, words, characters, and bytes in stdin"""
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
                f"  1   1   6   6 {path1}\n".encode(),
                b"  0   2  10  10\n",
                f"  1   3  18  27 {path2}\n".encode(),
                f"  0   0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0   0   0\n",
                f"  6  69 447 447 {path3}\n".encode(),
                f"  0   0   0   0 {random_filename} (no such file or directory)\n".encode(),
                b"  8  75 481 490 total\n",
            ])
            command = [
                "wordcount", "--lines", "--words", "--chars", "--bytes",
                path1, "-", path2, fake_dir, "-", path3, random_filename
            ]
            process = run(command, capture_output=True, input=b"flat white")
            assert process.stdout == expected

    @pytest.mark.timeout(TEST_TIMEOUT_SECONDS * 2)
    def test_always_displays_counts_in_the_same_order(self, make_file, fake_dir, random_filename):
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
                f"  1   1   6   6 {path1}\n".encode(),
                b"  0   2  10  10\n",
                f"  1   3  18  27 {path2}\n".encode(),
                f"  0   0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                b"  0   0   0   0\n",
                f"  6  69 447 447 {path3}\n".encode(),
                f"  0   0   0   0 {random_filename} (no such file or directory)\n".encode(),
                b"  8  75 481 490 total\n",
            ])
            for flags in permutations(["--lines", "--words", "--chars", "--bytes"]):
                command = [
                    "wordcount", *flags,
                    path1, "-", path2, fake_dir, "-", path3, random_filename
                ]
                process = run(command, capture_output=True, input=b"flat white")
                assert process.stdout == expected
