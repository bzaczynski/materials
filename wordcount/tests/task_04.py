from realpython import task


@task(
    number=4,
    name="Format Numbers in Displayed Counts",
    url="https://realpython.com/lessons/wordcount-format-numbers-in-displayed-counts-task/",
)
class Test:
    def test_long_word_without_trailing_newline(self, wc):
        assert b" 0  1 29\n" == wc(stdin=b"floccinaucinihilipilification")

    def test_long_word_with_trailing_newline(self, wc):
        assert b" 1  1 30\n" == wc(stdin=b"floccinaucinihilipilification\n")

    def test_multiple_words_without_trailing_newline(self, wc):
        assert b" 0  5 26\n" == wc(stdin=b"Lorem ipsum dolor sit amet")

    def test_multiple_words_with_trailing_newline(self, wc):
        assert b" 1  5 27\n" == wc(stdin=b"Lorem ipsum dolor sit amet\n")

    def test_long_text_multiple_lines(self, wc):
        assert b"  6  69 447\n" == wc(
            stdin=(
                b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\n"
                b"tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\n"
                b"quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\n"
                b"consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\n"
                b"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\n"
                b"proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
            )
        )
