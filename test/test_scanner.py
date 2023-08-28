from app.scanner import Scanner

from .helpers import *

scanner = Scanner()


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_scanner_discovers_files_to_be_transferred():
    create_valid_files()

    files_to_transfer = scanner.scan_dirs(dynamic_source_directory)

    assert sorted(list(files_to_transfer)) == valid_source_filepaths()


def test_scanner_ignores_files_without_desired_extensions():
    create_valid_files()
    undesired_files = [
        dynamic_source_directory + "sales.zip",
        dynamic_source_directory + "sales.rar",
        dynamic_source_directory + "sales.bin",
        ]
    for file in undesired_files:
        open(file, 'x').close()

    files_to_transfer = scanner.scan_dirs(dynamic_source_directory)

    assert sorted(list(files_to_transfer)) == valid_source_filepaths()


def test_copies_file_when_provided_source_path_does_not_have_backslash_as_final_char():
    create_valid_files()
    source_directory = static_source_directory[0:-1]
    files_to_transfer = scanner.scan_dirs(source_directory)
    expected_filepath = static_source_directory + 'a_file___1.jpeg'

    assert sorted(list(files_to_transfer)) == [expected_filepath]
