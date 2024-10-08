from subprocess import run

from realpython import task


@task(
    number=3,
    name="Handle non-ASCII Unicode Characters",
    url="TODO",
)
class Test:
    def test_short_unicode_word_no_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"caff\xc3\xa8")
        assert process.stdout == b"0 1 6\n"

    def test_short_unicode_word_with_trailing_newline(self):
        process = run(["wordcount"], capture_output=True, input=b"caff\xc3\xa8\n")
        assert process.stdout == b"1 1 7\n"
