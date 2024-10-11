from subprocess import run

from realpython import assert_equals, task


@task(
    number=2,
    name="Read Data from Standard Input",
    url="TODO",
)
class Test:
    def test_reports_zeros_on_an_empty_stream(self):
        process = run(["wordcount"], capture_output=True)
        assert_equals(b"0 0 0\n", process.stdout)

    def test_handles_a_short_word_without_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"caffe")
        assert b"0 1 5\n" == process.stdout

    def test_handles_a_short_word_with_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"caffe\n")
        assert b"1 1 6\n" == process.stdout

    def test_delimits_words_on_whitespace(self):
        process = run(["wordcount"], capture_output=True, input=b"back-end\n")
        assert b"1 1 9\n" == process.stdout, "Pay attention to punctuation and special characters"

    def test_handles_linux_newline(self):
        r"""Handles the Linux newline (\n)"""
        process = run(["wordcount"], capture_output=True, input=b"hot\ntea")
        assert b"1 2 7\n" == process.stdout

    def test_handles_macos_newline(self):
        r"""Handles the macOS newline (\r)"""
        process = run(["wordcount"], capture_output=True, input=b"hot\rtea")
        assert b"0 2 7\n" == process.stdout

    def test_handles_windows_newline(self):
        r"""Handles the Windows newline (\r\n)"""
        process = run(["wordcount"], capture_output=True, input=b"hot\r\ntea")
        assert b"1 2 8\n" == process.stdout
