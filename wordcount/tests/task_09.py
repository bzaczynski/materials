from itertools import permutations

from realpython import assert_equals, task


@task(
    number=9,
    name="Select Counts With Command-Line Options",
    url="TODO",
)
class Test:
    def test_counts_lines_words_bytes_by_default(
            self, wc, small_file, unicode_file, big_file, fake_dir, random_name
    ):
        """Counts lines, words, and bytes by default"""
        fixtures = [wc, small_file, unicode_file, big_file, fake_dir, random_name]
        assert_equals(b" 3  4 23\n", wc(stdin=b"caffe\nlatte\nflat white\n"))
        assert_equals(
            expected=b"".join(
                [
                    small_file.format_line(max_digits=3),
                    b"  0   2  10\n",
                    unicode_file.format_line(max_digits=3),
                    f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0   0\n",
                    big_file.format_line(max_digits=3),
                    f"  0   0   0 {random_name} (no such file or directory)\n".encode(),
                    b"  8  75 490 total\n",
                ]
            ),
            actual=run(*fixtures)
        )

    def test_counts_lines_words_bytes_explicitly(
            self, wc, small_file, unicode_file, big_file, fake_dir, random_name
    ):
        """Counts lines, words, and bytes explicitly"""
        fixtures = [wc, small_file, unicode_file, big_file, fake_dir, random_name]
        flags = ["--lines", "--words", "--bytes"]
        assert_equals(b" 3  4 23\n", wc(*flags, stdin=b"caffe\nlatte\nflat white\n"))
        assert_equals(
            expected=b"".join(
                [
                    small_file.format_line(max_digits=3),
                    b"  0   2  10\n",
                    unicode_file.format_line(max_digits=3),
                    f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
                    b"  0   0   0\n",
                    big_file.format_line(max_digits=3),
                    f"  0   0   0 {random_name} (no such file or directory)\n".encode(),
                    b"  8  75 490 total\n",
                ]
            ),
            actual=run(*fixtures, *flags)
        )

    def test_only_counts_lines(self, wc, small_file, unicode_file, big_file, fake_dir, random_name):
        fixtures = [wc, small_file, unicode_file, big_file, fake_dir, random_name]
        flags = ["--lines"]
        assert_equals(b"3\n", wc(*flags, stdin=b"caffe\nlatte\nflat white\n"))
        assert_equals(
            expected=b"".join(
                [
                    small_file.format_line(selected=8),
                    b"0\n",
                    unicode_file.format_line(selected=8),
                    f"0 {fake_dir}/ (is a directory)\n".encode(),
                    b"0\n",
                    big_file.format_line(selected=8),
                    f"0 {random_name} (no such file or directory)\n".encode(),
                    b"8 total\n",
                ]
            ),
            actual=run(*fixtures, *flags)
        )

    # def test_only_counts_words(self, wc, make_file, fake_dir, random_filename):
    #     assert b"4\n" == wc("--words", stdin=b"caffe\nlatte\nflat white\n")
    #     with (
    #         make_file(b"short\n") as path1,
    #         make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path2,
    #         make_file(
    #             b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\n"
    #             b"tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\n"
    #             b"quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\n"
    #             b"consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\n"
    #             b"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\n"
    #             b"proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
    #         ) as path3,
    #     ):
    #         assert b"".join(
    #             [
    #                 f" 1 {path1}\n".encode(),
    #                 b" 2\n",
    #                 f" 3 {path2}\n".encode(),
    #                 f" 0 {fake_dir}/ (is a directory)\n".encode(),
    #                 b" 0\n",
    #                 f"69 {path3}\n".encode(),
    #                 f" 0 {random_filename} (no such file or directory)\n".encode(),
    #                 b"75 total\n",
    #             ]
    #         ) == wc(
    #             "--words",
    #             path1,
    #             "-",
    #             path2,
    #             fake_dir,
    #             "-",
    #             path3,
    #             random_filename,
    #             stdin=b"flat white",
    #         )
    #
    # def test_only_counts_bytes(self, wc, make_file, fake_dir, random_filename):
    #     assert b"23\n" == wc("--bytes", stdin=b"caffe\nlatte\nflat white\n")
    #     with (
    #         make_file(b"short\n") as path1,
    #         make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path2,
    #         make_file(
    #             b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\n"
    #             b"tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\n"
    #             b"quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\n"
    #             b"consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\n"
    #             b"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\n"
    #             b"proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
    #         ) as path3,
    #     ):
    #         assert b"".join(
    #             [
    #                 f"  6 {path1}\n".encode(),
    #                 b" 10\n",
    #                 f" 27 {path2}\n".encode(),
    #                 f"  0 {fake_dir}/ (is a directory)\n".encode(),
    #                 b"  0\n",
    #                 f"447 {path3}\n".encode(),
    #                 f"  0 {random_filename} (no such file or directory)\n".encode(),
    #                 b"490 total\n",
    #             ]
    #         ) == wc(
    #             "--bytes",
    #             path1,
    #             "-",
    #             path2,
    #             fake_dir,
    #             "-",
    #             path3,
    #             random_filename,
    #             stdin=b"flat white",
    #         )
    #
    # def test_counts_lines_and_words(
    #     self, wc, make_file, fake_dir, random_filename
    # ):
    #     assert b"3 4\n" == wc(
    #         "--lines", "--words", stdin=b"caffe\nlatte\nflat white\n"
    #     )
    #     with (
    #         make_file(b"short\n") as path1,
    #         make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path2,
    #         make_file(
    #             b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\n"
    #             b"tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\n"
    #             b"quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\n"
    #             b"consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\n"
    #             b"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\n"
    #             b"proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
    #         ) as path3,
    #     ):
    #         assert b"".join(
    #             [
    #                 f" 1  1 {path1}\n".encode(),
    #                 b" 0  2\n",
    #                 f" 1  3 {path2}\n".encode(),
    #                 f" 0  0 {fake_dir}/ (is a directory)\n".encode(),
    #                 b" 0  0\n",
    #                 f" 6 69 {path3}\n".encode(),
    #                 f" 0  0 {random_filename} (no such file or directory)\n".encode(),
    #                 b" 8 75 total\n",
    #             ]
    #         ) == wc(
    #             "--lines",
    #             "--words",
    #             path1,
    #             "-",
    #             path2,
    #             fake_dir,
    #             "-",
    #             path3,
    #             random_filename,
    #             stdin=b"flat white",
    #         )
    #
    # def test_counts_lines_and_bytes(
    #     self, wc, make_file, fake_dir, random_filename
    # ):
    #     assert b" 3 23\n" == wc(
    #         "--lines", "--bytes", stdin=b"caffe\nlatte\nflat white\n"
    #     )
    #     with (
    #         make_file(b"short\n") as path1,
    #         make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path2,
    #         make_file(
    #             b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\n"
    #             b"tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\n"
    #             b"quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\n"
    #             b"consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\n"
    #             b"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\n"
    #             b"proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
    #         ) as path3,
    #     ):
    #         assert b"".join(
    #             [
    #                 f"  1   6 {path1}\n".encode(),
    #                 b"  0  10\n",
    #                 f"  1  27 {path2}\n".encode(),
    #                 f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
    #                 b"  0   0\n",
    #                 f"  6 447 {path3}\n".encode(),
    #                 f"  0   0 {random_filename} (no such file or directory)\n".encode(),
    #                 b"  8 490 total\n",
    #             ]
    #         ) == wc(
    #             "--lines",
    #             "--bytes",
    #             path1,
    #             "-",
    #             path2,
    #             fake_dir,
    #             "-",
    #             path3,
    #             random_filename,
    #             stdin=b"flat white",
    #         )
    #
    # def test_counts_words_and_bytes(
    #     self, wc, make_file, fake_dir, random_filename
    # ):
    #     assert b" 4 23\n" == wc(
    #         "--words", "--bytes", stdin=b"caffe\nlatte\nflat white\n"
    #     )
    #     with (
    #         make_file(b"short\n") as path1,
    #         make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path2,
    #         make_file(
    #             b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\n"
    #             b"tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\n"
    #             b"quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\n"
    #             b"consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\n"
    #             b"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\n"
    #             b"proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
    #         ) as path3,
    #     ):
    #         assert b"".join(
    #             [
    #                 f"  1   6 {path1}\n".encode(),
    #                 b"  2  10\n",
    #                 f"  3  27 {path2}\n".encode(),
    #                 f"  0   0 {fake_dir}/ (is a directory)\n".encode(),
    #                 b"  0   0\n",
    #                 f" 69 447 {path3}\n".encode(),
    #                 f"  0   0 {random_filename} (no such file or directory)\n".encode(),
    #                 b" 75 490 total\n",
    #             ]
    #         ) == wc(
    #             "--words",
    #             "--bytes",
    #             path1,
    #             "-",
    #             path2,
    #             fake_dir,
    #             "-",
    #             path3,
    #             random_filename,
    #             stdin=b"flat white",
    #         )
    #
    # def test_always_displays_counts_in_the_same_order(
    #     self, wc, make_file, fake_dir, random_filename
    # ):
    #     with (
    #         make_file(b"short\n") as path1,
    #         make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path2,
    #         make_file(
    #             b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\n"
    #             b"tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\n"
    #             b"quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\n"
    #             b"consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\n"
    #             b"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\n"
    #             b"proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
    #         ) as path3,
    #     ):
    #         expected = b"".join(
    #             [
    #                 f"  1   1   6 {path1}\n".encode(),
    #                 b"  0   2  10\n",
    #                 f"  1   3  27 {path2}\n".encode(),
    #                 f"  0   0   0 {fake_dir}/ (is a directory)\n".encode(),
    #                 b"  0   0   0\n",
    #                 f"  6  69 447 {path3}\n".encode(),
    #                 f"  0   0   0 {random_filename} (no such file or directory)\n".encode(),
    #                 b"  8  75 490 total\n",
    #             ]
    #         )
    #         for flags in permutations(["--lines", "--words", "--bytes"]):
    #             assert b" 3  4 23\n" == wc(
    #                 *flags, stdin=b"caffe\nlatte\nflat white\n"
    #             )
    #             assert expected == wc(
    #                 *flags,
    #                 path1,
    #                 "-",
    #                 path2,
    #                 fake_dir,
    #                 "-",
    #                 path3,
    #                 random_filename,
    #                 stdin=b"flat white",
    #             )


def run(wc, file1, file2, file3, fake_dir, random_name, *flags):
    return wc(
        *flags,
        str(file1.path),
        "-",
        str(file2.path),
        fake_dir,
        "-",
        str(file3.path),
        random_name,
        stdin=b"flat white",
    )
