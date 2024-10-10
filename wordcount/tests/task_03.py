from subprocess import run

from realpython import task


@task(
    number=3,
    name="Handle Non-ASCII Unicode Characters",
    url="TODO",
)
class Test:
    def test_decodes_multibyte_character_without_trailing_newline(self):
        """Decodes a multi-byte character without a trailing newline"""
        process = run(["wordcount"], capture_output=True, input=b"caff\xc3\xa8")
        assert process.stdout == b"0 1 6\n"

    def test_decodes_multibyte_character_with_trailing_newline(self):
        """Decodes a multi-byte character with a trailing newline"""
        process = run(["wordcount"], capture_output=True, input=b"caff\xc3\xa8\n")
        assert process.stdout == b"1 1 7\n"
