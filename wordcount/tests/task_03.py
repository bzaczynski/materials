from realpython import task


@task(
    number=3,
    name="Handle Non-ASCII Unicode Characters",
    url="TODO",
)
class Test:
    def test_decodes_multibyte_character_without_trailing_newline(self, wc):
        """Decodes a multi-byte character without a trailing newline"""
        assert b"0 1 6\n" == wc(
            stdin=b"caff\xc3\xa8"
        ), b"Note the difference between _e_ and _\xc3\xa8_, for example.".decode(
            "utf-8"
        )

    def test_decodes_multibyte_character_with_trailing_newline(self, wc):
        """Decodes a multi-byte character with a trailing newline"""
        assert b"1 1 7\n" == wc(stdin=b"caff\xc3\xa8\n")
