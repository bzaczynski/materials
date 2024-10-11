from itertools import permutations

from realpython import task


@task(
    number=9,
    name="Select Counts With Command-Line Options",
    url="TODO",
)
class Test:
    def test_counts_lines_words_bytes_by_default(
        self, wc, make_file, fake_dir, random_filename
    ):
        """Counts lines, words, and bytes by default"""
        assert b" 3  4 23\n" == wc(stdin=b"caffe\nlatte\nflat white\n")
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
                    f"  1   3  27 {path2}\n".encode(),
                    f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0   0\n",
                    f"  6  69 447 {path3}\n".encode(),
                    f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                    b"  8  75 490 total\n",
                ]
            ) == wc(
                path1,
                "-",
                path2,
                fake_dir,
                "-",
                path3,
                random_filename,
                stdin=b"flat white",
            )

    def test_counts_lines_words_bytes_explicitly(
        self, wc, make_file, fake_dir, random_filename
    ):
        """Counts lines, words, and bytes explicitly"""
        assert b" 3  4 23\n" == wc(
            "--lines",
            "--words",
            "--bytes",
            stdin=b"caffe\nlatte\nflat white\n",
        )
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
                    f"  1   3  27 {path2}\n".encode(),
                    f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0   0\n",
                    f"  6  69 447 {path3}\n".encode(),
                    f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                    b"  8  75 490 total\n",
                ]
            ) == wc(
                "--lines",
                "--words",
                "--bytes",
                path1,
                "-",
                path2,
                fake_dir,
                "-",
                path3,
                random_filename,
                stdin=b"flat white",
            )

    def test_only_counts_lines(self, wc, make_file, fake_dir, random_filename):
        assert b"3\n" == wc("--lines", stdin=b"caffe\nlatte\nflat white\n")
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
                    f"1 {path1}\n".encode(),
                    b"0\n",
                    f"1 {path2}\n".encode(),
                    f"0 {fake_dir}/ (is a directory)\n".encode(),
                    b"0\n",
                    f"6 {path3}\n".encode(),
                    f"0 {random_filename} (no such file or directory)\n".encode(),
                    b"8 total\n",
                ]
            ) == wc(
                "--lines",
                path1,
                "-",
                path2,
                fake_dir,
                "-",
                path3,
                random_filename,
                stdin=b"flat white",
            )

    def test_only_counts_words(self, wc, make_file, fake_dir, random_filename):
        assert b"4\n" == wc("--words", stdin=b"caffe\nlatte\nflat white\n")
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
                    f" 1 {path1}\n".encode(),
                    b" 2\n",
                    f" 3 {path2}\n".encode(),
                    f" 0 {fake_dir}/ (is a directory)\n".encode(),
                    b" 0\n",
                    f"69 {path3}\n".encode(),
                    f" 0 {random_filename} (no such file or directory)\n".encode(),
                    b"75 total\n",
                ]
            ) == wc(
                "--words",
                path1,
                "-",
                path2,
                fake_dir,
                "-",
                path3,
                random_filename,
                stdin=b"flat white",
            )

    def test_only_counts_bytes(self, wc, make_file, fake_dir, random_filename):
        assert b"23\n" == wc("--bytes", stdin=b"caffe\nlatte\nflat white\n")
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
                    f" 27 {path2}\n".encode(),
                    f"  0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0\n",
                    f"447 {path3}\n".encode(),
                    f"  0 {random_filename} (no such file or directory)\n".encode(),
                    b"490 total\n",
                ]
            ) == wc(
                "--bytes",
                path1,
                "-",
                path2,
                fake_dir,
                "-",
                path3,
                random_filename,
                stdin=b"flat white",
            )

    def test_counts_lines_and_words(
        self, wc, make_file, fake_dir, random_filename
    ):
        assert b"3 4\n" == wc(
            "--lines", "--words", stdin=b"caffe\nlatte\nflat white\n"
        )
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
                    f" 1  1 {path1}\n".encode(),
                    b" 0  2\n",
                    f" 1  3 {path2}\n".encode(),
                    f" 0  0 {fake_dir}/ (is a directory)\n".encode(),
                    b" 0  0\n",
                    f" 6 69 {path3}\n".encode(),
                    f" 0  0 {random_filename} (no such file or directory)\n".encode(),
                    b" 8 75 total\n",
                ]
            ) == wc(
                "--lines",
                "--words",
                path1,
                "-",
                path2,
                fake_dir,
                "-",
                path3,
                random_filename,
                stdin=b"flat white",
            )

    def test_counts_lines_and_bytes(
        self, wc, make_file, fake_dir, random_filename
    ):
        assert b" 3 23\n" == wc(
            "--lines", "--bytes", stdin=b"caffe\nlatte\nflat white\n"
        )
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
                    f"  1  27 {path2}\n".encode(),
                    f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0\n",
                    f"  6 447 {path3}\n".encode(),
                    f"  0   0 {random_filename} (no such file or directory)\n".encode(),
                    b"  8 490 total\n",
                ]
            ) == wc(
                "--lines",
                "--bytes",
                path1,
                "-",
                path2,
                fake_dir,
                "-",
                path3,
                random_filename,
                stdin=b"flat white",
            )

    def test_counts_words_and_bytes(
        self, wc, make_file, fake_dir, random_filename
    ):
        assert b" 4 23\n" == wc(
            "--words", "--bytes", stdin=b"caffe\nlatte\nflat white\n"
        )
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
                    f"  3  27 {path2}\n".encode(),
                    f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0\n",
                    f" 69 447 {path3}\n".encode(),
                    f"  0   0 {random_filename} (no such file or directory)\n".encode(),
                    b" 75 490 total\n",
                ]
            ) == wc(
                "--words",
                "--bytes",
                path1,
                "-",
                path2,
                fake_dir,
                "-",
                path3,
                random_filename,
                stdin=b"flat white",
            )

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
                    f"  1   1   6 {path1}\n".encode(),
                    b"  0   2  10\n",
                    f"  1   3  27 {path2}\n".encode(),
                    f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0   0\n",
                    f"  6  69 447 {path3}\n".encode(),
                    f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
                    b"  8  75 490 total\n",
                ]
            )
            for flags in permutations(["--lines", "--words", "--bytes"]):
                assert b" 3  4 23\n" == wc(
                    *flags, stdin=b"caffe\nlatte\nflat white\n"
                )
                assert expected == wc(
                    *flags,
                    path1,
                    "-",
                    path2,
                    fake_dir,
                    "-",
                    path3,
                    random_filename,
                    stdin=b"flat white",
                )
