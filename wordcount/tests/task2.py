from subprocess import run

import pytest

from realpython import task


@task(
    number=2,
    name="Read Data from Standard Input",
    url="TODO",
)
class Test:
    def test_empty_stream(self):
        process = run(["wordcount"], capture_output=True)
        assert process.stdout == b"0 0 0\n"

    def test_short_word_no_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"caffe")
        assert process.stdout == b"0 1 5\n"

    def test_short_word_with_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"caffe\n")
        assert process.stdout == b"1 1 6\n"

    def test_long_word_no_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"floccinaucinihilipilification")
        assert process.stdout == b" 0  1 29\n"

    def test_long_word_with_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"floccinaucinihilipilification\n")
        assert process.stdout == b" 1  1 30\n"

    def test_multiple_words_no_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"Lorem ipsum dolor sit amet")
        assert process.stdout == b" 0  5 26\n"

    def test_multiple_words_with_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"Lorem ipsum dolor sit amet\n")
        assert process.stdout == b" 1  5 27\n"

    def test_long_text_multiple_lines(self):
        process = run(["wordcount"], capture_output=True, input=(
            b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\n"
            b"tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\n"
            b"quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\n"
            b"consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\n"
            b"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\n"
            b"proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
        ))
        assert process.stdout == b"  6  69 447\n"

    # TODO split this into separate tasks? i.e., formatting, bytes vs chars, etc.

    # TODO \n vs \r vs \r\n (????)
    # TODO special characters...
    # TODO non-printable characters

    # @pytest.mark.parametrize(
    #     "word, expected",
    #     [
    #         (b"caffe", b"0 1 5\n"),
    #         (b"caffe latte", b" 0  2 11\n"),
    #     ],
    # )
    # def test_reads_single_line_no_trailing_newline(self, word, expected):
    #     process = run(["wordcount"], input=word, capture_output=True)
    #     #assert process.stdout == expected
    #     print(process.stdout)


    # """
    #             (b"caffe\n", b"1 1 6\n"),
    #         (b"caffe latte\n", b"1 2 12\n"),
    # reprehenderit
    # exercitation
    # consectetur
    # incididunt
    # consequat
    # pariatur
    # proident
    # eiusmod
    # nostrud
    # tempor
    # amet
    # et
    # """
    #
    # @pytest.mark.parametrize(
    #     "word, expected_output",
    #     [
    #         (b"reprehenderit", b"1 1 13\n"),
    #         # (b"caffe", b"1 2 11\n"),
    #         # (b"caffe\nlatte", b"2 2 12\n"),
    #     ],
    # )
    # def test_reads_one_word(self, word, expected_output):
    #     process = run(["wordcount"], input=word, capture_output=True)
    #     #assert process.stdout == b"0 0 0\n"
    #     print(">>>", repr(process.stdout))

    # read multiple lines

    # def test_reads_one_word_from_stdin(self):
    #     process = run(["wordcount"], capture_output=True, input=b"caffe")
    #     assert process.stdout == b"1 1 6"
    #     print(">>>", repr(process.stdout))

    # def test_reads_bytes_from_stdin(self):
    #     process = run(["wordcount"], capture_output=True, input=b"caffe latte\n")
    #     print(">>>", repr(process.stdout))
    #     assert process.returncode == 0

    # def test_prints_lines_words_bytes(self):
    #     ...
    # PIPE?
