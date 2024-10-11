from realpython import task


@task(
    number=11,
    name="Foo",
    url="Nasas"
)
class Test:
    def test_foo(self, file1):
        print(">>>", file1, file1.path)
