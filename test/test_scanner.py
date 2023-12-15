from app.scanner import Scanner

from .helpers import *

scanner = Scanner()


@pytest.fixture(autouse=True)
def teardown():
    clear_test_directories()


def test_scanner_discovers_files_to_be_copied():
    create_files_with_desired_extensions()

    files_to_copy = scanner.valid_filepaths_in(source_directory)

    assert sorted(list(files_to_copy)) == valid_source_filepaths()


def test_scanner_ignores_files_without_desired_extensions():
    create_files_with_desired_extensions()
    create_files_without_desired_extensions()

    files_to_copy = scanner.valid_filepaths_in(source_directory)

    assert sorted(list(files_to_copy)) == valid_source_filepaths()


def test_copies_file_when_provided_source_path_does_not_have_trailing_backslash():
    filename = 'a_file.jpeg'
    source_filepath = create_file(source_directory, filename)
    source_directory_without_trailing_backslash = source_directory[0:-1]
    files_to_copy = scanner.valid_filepaths_in(source_directory_without_trailing_backslash)

    assert list(files_to_copy) == [source_filepath]


def test_provides_a_set_of_invalid_file_extensions():
    create_file(source_directory, 'a_file.non')
    create_file(source_directory, 'a_file_2.non')
    result = scanner.invalid_extensions_in(source_directory)
    extension = '.non'

    assert list(result) == [extension]
    assert len(list(result)) == 1


def test_provides_multiple_invalid_extensions():
    create_file(source_directory, 'a_file.non')
    create_file(source_directory, 'a_file_2.hlp')
    result = scanner.invalid_extensions_in(source_directory)
    extensions = sorted(['.non', '.hlp'])

    assert sorted(list(result)) == extensions
