from app.scanner import Scanner

from .helpers import *

scanner = Scanner()


@pytest.fixture(autouse=True)
def teardown():
    clear_test_directories()


def test_scanner_discovers_files_to_be_transferred():
    create_files_with_desired_extensions()

    files_to_transfer = scanner.scan_directory(source_directory)

    assert sorted(list(files_to_transfer)) == valid_source_filepaths()


def test_scanner_ignores_files_without_desired_extensions():
    create_files_with_desired_extensions()
    create_files_without_desired_extensions()

    files_to_transfer = scanner.scan_directory(source_directory)

    assert sorted(list(files_to_transfer)) == valid_source_filepaths()


def test_copies_file_when_provided_source_path_does_not_have_trailing_backslash():
    filename = 'a_file.jpeg'
    source_filepath = create_file(source_directory, filename)
    source_directory_without_trailing_backslash = source_directory[0:-1]
    files_to_transfer = scanner.scan_directory(source_directory_without_trailing_backslash)

    assert list(files_to_transfer) == [source_filepath]
