from subprocess import run

from realpython import course, task, tutorial


@task(
    number=1,
    name="Run the wordcount Command",
    url="https://realpython.com/lessons/run-the-wordcount-command-task/",
)
@tutorial("python-comments-guide")
@course("writing-comments-python", "Writing Comments in Python")
class Test:
    def test_command_returns_successfully(self):
        process = run(["wordcount", "/dev/null"], capture_output=True)
        assert process.returncode == 0
