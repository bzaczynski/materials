from realpython import task


@task(
    number=6,
    name="Ignore Directories and Missing Files",
    url="TODO",
)
class Test:
    def test_reports_zeros_on_a_directory(self, wc, fake_dir):
        assert f"0 0 0 {fake_dir}/ (is a directory)\n".encode() == wc(fake_dir)

    def test_reports_zeros_on_a_missing_file(self, wc, random_filename):
        assert (
            f"0 0 0 {random_filename} (no such file or directory)\n".encode()
            == wc(random_filename)
        )
