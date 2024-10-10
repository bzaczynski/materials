from subprocess import run

import pytest

from realpython import task


@task(
    number=10,
    name="Add Support for Counting Characters",
    url="TODO",
)
class Test:
    def test_foo(self):
        pytest.fail()
