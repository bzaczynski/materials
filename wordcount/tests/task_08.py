from realpython import task


@task(
    number=8,
    name="Ensure Consistent Number Formatting",
    url="TODO",
)
class Test:
    def test_uses_consistent_formatting_across_lines(
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
            assert expected == wc(
                path1,
                "-",
                path2,
                fake_dir,
                "-",
                path3,
                random_filename,
                stdin=b"flat white",
            )
