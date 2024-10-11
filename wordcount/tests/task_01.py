import os
from subprocess import run

from realpython import assert_equals, course, task, tutorial


@task(
    number=1,
    name="Run the wordcount Command",
    url="https://realpython.com/lessons/run-the-wordcount-command-task/",
)
@tutorial("python-comments-guide")
@course("writing-comments-python", "Writing Comments in Python")
class Test:
    def test_command_returns_successfully(self):
        process = run(["wordcount", os.devnull], capture_output=True)
        assert_equals(
            expected=0,
            actual=process.returncode,
            message=(
                "The process should return a zero [exit status]"
                "(https://en.wikipedia.org/wiki/Exit_status) code"
            )
        )
