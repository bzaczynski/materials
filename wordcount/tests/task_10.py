from itertools import permutations

import pytest
from realpython import TEST_TIMEOUT_SECONDS, task


@task(
    number=10,
    name="Add Support for Counting the Characters",
    url="TODO",
)
class Test:
    def test_only_counts_characters(
        self, wc, make_file, fake_dir, random_filename
    ):
        assert b"18\n" == wc("--chars", stdin="zażółć\ngęślą\njaźń\n".encode("utf-8"))
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
            assert b"".join(
                [
                    f"  6 {path1}\n".encode(),
                    b" 10\n",
                    f" 18 {path2}\n".encode(),
                    f"  0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0\n",
                    f"447 {path3}\n".encode(),
                    f"  0 {random_filename} (no such file or directory)\n".encode(),
                    b"481 total\n",
                ]
            ) == wc("--chars", path1, "-", path2, fake_dir, "-", path3, random_filename, stdin=b"flat white")

    def test_counts_characters_and_bytes(self, wc, make_file, fake_dir, random_filename):
        assert b"18 27\n" == wc("--chars", "--bytes", stdin="zażółć\ngęślą jaźń\n".encode("utf-8"))
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
            assert b"".join(
                [
                    f"  6   6 {path1}\n".encode(),
                    b" 10  10\n",
                    f" 18  27 {path2}\n".encode(),
                    f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0\n",
                    f"447 447 {path3}\n".encode(),
                    f"  0   0 {random_filename} (no such file or directory)\n".encode(),
                    b"481 490 total\n",
                ]
            ) == wc("--chars", "--bytes", path1, "-", path2, fake_dir, "-", path3, random_filename, stdin=b"flat white")

    def test_counts_words_and_characters(
        self, wc, make_file, fake_dir, random_filename
    ):
        assert b" 3 18\n" == wc("--words", "--chars", stdin="zażółć\ngęślą jaźń\n".encode("utf-8"))
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
            assert b"".join(
                [
                    f"  1   6 {path1}\n".encode(),
                    b"  2  10\n",
                    f"  3  18 {path2}\n".encode(),
                    f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0\n",
                    f" 69 447 {path3}\n".encode(),
                    f"  0   0 {random_filename} (no such file or directory)\n".encode(),
                    b" 75 481 total\n",
                ]
            ) == wc("--words", "--chars", path1, "-", path2, fake_dir, "-", path3, random_filename, stdin=b"flat white")

    def test_counts_words_characters_bytes(
        self, wc, make_file, fake_dir, random_filename
    ):
        """Counts words, characters, and bytes in stdin"""
        assert b" 3 18 27\n" == wc("--words", "--chars", "--bytes", stdin="zażółć\ngęślą jaźń\n".encode("utf-8"))
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
            assert b"".join(
                [
                    f"  1   6   6 {path1}\n".encode(),
                    b"  2  10  10\n",
                    f"  3  18  27 {path2}\n".encode(),
                    f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0   0\n",
                    f" 69 447 447 {path3}\n".encode(),
                    f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                    b" 75 481 490 total\n",
                ]
            ) == wc("--words", "--chars", "--bytes", path1, "-", path2, fake_dir, "-", path3, random_filename, stdin=b"flat white")

    def test_counts_lines_and_characters(
        self, wc, make_file, fake_dir, random_filename
    ):
        assert b" 2 18\n" == wc("--lines", "--chars", stdin="zażółć\ngęślą jaźń\n".encode("utf-8"))
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
            assert b"".join(
                [
                    f"  1   6 {path1}\n".encode(),
                    b"  0  10\n",
                    f"  1  18 {path2}\n".encode(),
                    f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0\n",
                    f"  6 447 {path3}\n".encode(),
                    f"  0   0 {random_filename} (no such file or directory)\n".encode(),
                    b"  8 481 total\n",
                ]
            ) == wc("--lines", "--chars", path1, "-", path2, fake_dir, "-", path3, random_filename, stdin=b"flat white")

    def test_counts_lines_characters_bytes(
        self, wc, make_file, fake_dir, random_filename
    ):
        """Counts lines, characters, and bytes in stdin"""
        assert b" 2 18 27\n" == wc("--lines", "--chars", "--bytes", stdin="zażółć\ngęślą jaźń\n".encode("utf-8"))
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
            assert b"".join(
                [
                    f"  1   6   6 {path1}\n".encode(),
                    b"  0  10  10\n",
                    f"  1  18  27 {path2}\n".encode(),
                    f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0   0\n",
                    f"  6 447 447 {path3}\n".encode(),
                    f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                    b"  8 481 490 total\n",
                ]
            ) == wc("--lines", "--chars", "--bytes", path1, "-", path2, fake_dir, "-", path3, random_filename, stdin=b"flat white")

    def test_counts_lines_words_characters(
        self, wc, make_file, fake_dir, random_filename
    ):
        """Counts lines, words, and characters in stdin"""
        assert b" 2  3 18\n" == wc("--lines", "--words", "--chars", stdin="zażółć\ngęślą jaźń\n".encode("utf-8"))
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
            assert b"".join(
                [
                    f"  1   1   6 {path1}\n".encode(),
                    b"  0   2  10\n",
                    f"  1   3  18 {path2}\n".encode(),
                    f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0   0\n",
                    f"  6  69 447 {path3}\n".encode(),
                    f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                    b"  8  75 481 total\n",
                ]
            ) == wc("--lines", "--words", "--chars", path1, "-", path2, fake_dir, "-", path3, random_filename, stdin=b"flat white")

    def test_counts_lines_words_characters_bytes(
        self, wc, make_file, fake_dir, random_filename
    ):
        """Counts lines, words, characters, and bytes in stdin"""
        assert b" 2  3 18 27\n" == wc("--lines", "--words", "--chars", "--bytes", stdin="zażółć\ngęślą jaźń\n".encode("utf-8"))
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
            assert b"".join(
                [
                    f"  1   1   6   6 {path1}\n".encode(),
                    b"  0   2  10  10\n",
                    f"  1   3  18  27 {path2}\n".encode(),
                    f"  0   0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0   0   0\n",
                    f"  6  69 447 447 {path3}\n".encode(),
                    f"  0   0   0   0 {random_filename} (no such file or directory)\n".encode(),
                    b"  8  75 481 490 total\n",
                ]
            ) == wc("--lines", "--words", "--chars", "--bytes", path1, "-", path2, fake_dir, "-", path3, random_filename, stdin=b"flat white")

    @pytest.mark.timeout(TEST_TIMEOUT_SECONDS * 2)
    def test_always_displays_counts_in_the_same_order(
        self, wc, make_file, fake_dir, random_filename
    ):
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
            expected = b"".join(
                [
                    f"  1   1   6   6 {path1}\n".encode(),
                    b"  0   2  10  10\n",
                    f"  1   3  18  27 {path2}\n".encode(),
                    f"  0   0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0   0   0\n",
                    f"  6  69 447 447 {path3}\n".encode(),
                    f"  0   0   0   0 {random_filename} (no such file or directory)\n".encode(),
                    b"  8  75 481 490 total\n",
                ]
            )
            for flags in permutations(
                ["--lines", "--words", "--chars", "--bytes"]
            ):
                assert b" 2  3 18 27\n" == wc(*flags, stdin="zażółć\ngęślą jaźń\n".encode("utf-8"))
                assert expected == wc(*flags, path1, "-", path2, fake_dir, "-", path3, random_filename, stdin=b"flat white")
