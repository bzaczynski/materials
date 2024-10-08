## Task 1 - Make `wordcount` runnable

Uncomment the main() function to make the `wordcount` command return successfully.

## Task 2 - Read From Stdin, count text

Read data from stdin and count the number of lines, words, and bytes using `sys.stding.read()` but without formatting.

## Task 3 - Add Unicode Support (bytes instead of characters)

Fix the count of bytes vs characters (non-ASCII Unicode).

## Task 4 - Add Formatting

...

## Task 5 - Read from a single file

...



---



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
