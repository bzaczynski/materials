from subprocess import run

from realpython import task


@task(
    number=2,
    name="Read Data from Standard Input",
    url="TODO",
)
class Test:
    def test_reports_zeros_on_empty_stream(self):
        process = run(["wordcount"], capture_output=True)
        assert process.stdout == b"0 0 0\n"

    def test_handles_short_word_without_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"caffe")
        assert process.stdout == b"0 1 5\n"

    def test_handles_short_word_with_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"caffe\n")
        assert process.stdout == b"1 1 6\n"

    def test_delimits_words_on_whitespace(self):
        process = run(["wordcount"], capture_output=True, input=b"back-end\n")
        assert process.stdout == b"1 1 9\n"

    def test_handles_linux_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"hot\ntea")
        assert process.stdout == b"1 2 7\n"

    def test_handles_macos_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"hot\rtea")
        assert process.stdout == b"0 2 7\n"

    def test_handles_windows_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"hot\r\ntea")
        assert process.stdout == b"1 2 8\n"
