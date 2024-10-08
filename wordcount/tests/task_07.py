from subprocess import run

from realpython import task


@task(
    number=7,
    name="Read Data From Multiple Files",
    url="TODO",
)
class Test:
    def test_display_counts_and_filenames_on_separate_lines(self, temporary_path_factory):
        contents = {
            b"caffe latte\n": b" 1  2 12",
            b"Lorem ipsum dolor sit amet\n": b" 1  5 27",
            "Zażółć gęślą jaźń\n".encode("utf-8"): b" 1  3 27",
        }
        paths = {
            temporary_path_factory(content): counts
            for content, counts in contents.items()
        }
        expected = b"".join(
            counts + b" " + str(path).encode() + b"\n"
            for path, counts in paths.items()
        )
        process = run(["wordcount", *paths], capture_output=True)
        assert process.stdout.startswith(expected)

    def test_include_a_summary_with_total_counts(self, temporary_path_factory):
        contents = {
            b"caffe latte\n": b" 1  2 12",
            b"Lorem ipsum dolor sit amet\n": b" 1  5 27",
            "Zażółć gęślą jaźń\n".encode("utf-8"): b" 1  3 27",
        }
        paths = {
            temporary_path_factory(content): counts
            for content, counts in contents.items()
        }
        process = run(["wordcount", *paths], capture_output=True)
        assert process.stdout.endswith(b" 3 10 66 total\n")

    def test_repeat_the_same_file(self, temporary_path_factory):
        ...

    # TODO mix stdin (-) with real filenames

    # TODO repeat the same file

    # TODO repeat stdin (-)

    # TODO don't show totals when one file

    # TODO show totals when more files

    # TODO Next up: formatting advanced?
    # TODO Next up: argparse
    # TODO Next up: counts selection
