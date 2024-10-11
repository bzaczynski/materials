from realpython import task


@task(
    number=7,
    name="Read Data From Multiple Files",
    url="TODO",
)
class Test:
    def test_displays_counts_and_filenames_on_separate_lines(
        self, wc, make_file
    ):
        with (
            make_file(b"caffe latte\n") as path1,
            make_file(b"Lorem ipsum dolor sit amet\n") as path2,
            make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path3,
        ):
            expected = b"".join(
                [
                    f" 1  2 12 {path1}\n".encode(),
                    f" 1  5 27 {path2}\n".encode(),
                    f" 1  3 27 {path3}\n".encode(),
                ]
            )
            assert wc(path1, path2, path3).startswith(expected)

    def test_includes_a_summary_with_total_counts(self, wc, make_file):
        with (
            make_file(b"caffe latte\n") as path1,
            make_file(b"Lorem ipsum dolor sit amet\n") as path2,
            make_file("Zażółć gęślą jaźń\n".encode("utf-8")) as path3,
        ):
            assert wc(path1, path2, path3).endswith(b" 3 10 66 total\n")

    def test_can_repeat_the_same_file_multiple_times(self, wc, make_file):
        with make_file(b"caffe latte\n") as path:
            expected = (
                f" 1  2 12 {path}\n"
                f" 1  2 12 {path}\n"
                f" 1  2 12 {path}\n"
                f" 3  6 36 total\n"
            )
            assert expected.encode() == wc(path, path, path)

    def test_can_mix_files_with_standard_input(self, wc, make_file):
        with make_file(b"Lorem ipsum dolor sit amet\n") as path:
            expected = f" 1  5 27 {path}\n 0  2 11\n 1  7 38 total\n"
            assert expected.encode() == wc(path, "-", stdin=b"caffe latte")

    # @pytest.mark.skip
    # def test_can_repeat_standard_input_multiple_times(self, make_file):
    #     pass

    def test_reports_a_directory_and_a_missing_file(
        self, wc, random_filename, fake_dir
    ):
        assert b"".join(
            [
                f"0 0 0 {fake_dir}/ (is a directory)\n".encode(),
                f"0 0 0 {random_filename} (no such file or directory)\n".encode(),
                b"0 0 0 total\n",
            ]
        ) == wc(fake_dir, random_filename)

    def test_reports_a_mix_of_all(
        self, wc, random_filename, fake_dir, make_file
    ):
        with make_file(b"caffe\n") as path:
            assert b"".join(
                [
                    f"0 0 0 {fake_dir}/ (is a directory)\n".encode(),
                    f"1 1 6 {path}\n".encode(),
                    f"0 0 0 {random_filename} (no such file or directory)\n".encode(),
                    b"0 1 3\n",
                    b"1 2 9 total\n",
                ]
            ) == wc(fake_dir, str(path), random_filename, "-", stdin=b"hot")
