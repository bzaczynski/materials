from subprocess import run

from realpython import task


@task(
    number=9,
    name="Select Counts With Command-Line Options",
    url="TODO",
)
class Test:
    pass

#     def test_uses_argparse_instead_of_sys_argv(self):
#         process = run(["wordcount", "--help"], capture_output=True)
#         assert (b"""\
# options:
#   -h, --help  show this help message and exit
# """) in process.stdout
#
#     def test_has_the_expected_options(self):
#         process = run(["wordcount", "--help"], capture_output=True)
#         for option in [b"--lines", b"--words", b"--bytes", b"--chars"]:
#             assert option in process.stdout
#
#     def test_shows_only_lines(self):
#         command = ["wordcount", "--lines", "-"]
#         process = run(command, capture_output=True, input=b"caffe\n")
#         # process.stdout
#         # TODO
