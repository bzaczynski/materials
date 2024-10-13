from realpython import assert_equals, assert_equals_if, task


@task(
    number=2,
    name="Read Data from Standard Input",
    url="https://realpython.com/lessons/wordcount-read-data-from-standard-input-task/",
)
class Test:
    def test_reports_zeros_on_an_empty_stream(self, wc):
        assert_equals(b"0 0 0\n", wc())

    def test_handles_a_short_word_without_trailing_newline(self, wc):
        assert_equals_if(b"0 1 5\n", wc(stdin=b"caffe"))

    def test_handles_a_short_word_with_trailing_newline(self, wc):
        assert_equals_if(b"1 1 6\n", wc(stdin=b"caffe\n"))

    def test_delimits_words_on_whitespace(self, wc):
        assert_equals_if(
            expected=b"1 1 9\n",
            actual=wc(stdin=b"back-end\n"),
            message="Pay attention to punctuation and special characters.",
        )

    def test_handles_linux_newline(self, wc):
        r"""Handles the Linux newline (\n)"""
        assert_equals_if(b"1 2 7\n", wc(stdin=b"hot\ntea"))

    def test_handles_macos_newline(self, wc):
        r"""Handles the macOS newline (\r)"""
        assert_equals_if(b"0 2 7\n", wc(stdin=b"hot\rtea"))

    def test_handles_windows_newline(self, wc):
        r"""Handles the Windows newline (\r\n)"""
        assert_equals_if(b"1 2 8\n", wc(stdin=b"hot\r\ntea"))
