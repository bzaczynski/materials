import textwrap

from realpython import task


@task(
    number=5,
    name="Read Data From a File",
    url="TODO",
)
class Test:
    def test_displays_counts_and_a_filename_on_the_same_line(
        self, wc, make_file
    ):
        with make_file(b"caffe latte\n") as path:
            assert f" 1  2 12 {path}\n".encode() == wc(
                str(path)
            ), textwrap.dedent(
                """\
                    Sample output:
                    
                    ```sh
                    $ wordcount ~/file.txt
                     1  2 12 /home/user/file.txt
                    ```
                    """
            )

    def test_treats_the_dash_character_as_standard_input(self, wc):
        """Treats the dash character (-) as standard input"""
        assert b"1 1 6\n" == wc("-", stdin=b"latte\n")
