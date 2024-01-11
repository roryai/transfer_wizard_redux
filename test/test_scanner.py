from app.scanner import Scanner, MEDIA_EXTENSIONS

from .helpers import *

scanner = Scanner()


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_scanner_discovers_files_to_be_copied():
    create_files_with_desired_extensions()

    files_to_copy = scanner.media_filepaths_in(source_directory)

    assert sorted(list(files_to_copy)) == media_source_filepaths()


def test_scanner_ignores_files_without_desired_extensions():
    create_files_with_desired_extensions()
    create_files_without_desired_extensions()

    files_to_copy = scanner.media_filepaths_in(source_directory)

    assert sorted(list(files_to_copy)) == media_source_filepaths()


def test_copies_file_when_provided_source_path_does_not_have_trailing_backslash():
    filename = 'a_file.jpeg'
    source_filepath = create_file(source_directory, filename)
    source_directory_without_trailing_backslash = source_directory[0:-1]
    files_to_copy = scanner.media_filepaths_in(source_directory_without_trailing_backslash)

    assert list(files_to_copy) == [source_filepath]


def test_does_not_provide_media_extensions_when_scanning_for_misc_extensions():
    create_file(source_directory, 'a_file.jpg')
    result = scanner.misc_extensions_in(source_directory)

    assert list(result) == []


def test_provides_a_set_of_misc_file_extensions():
    create_file(source_directory, 'a_file.non')
    create_file(source_directory, 'a_file_2.non')
    result = scanner.misc_extensions_in(source_directory)
    extension = '.non'

    assert list(result) == [extension]
    assert len(list(result)) == 1


def test_provides_multiple_misc_extensions():
    create_file(source_directory, 'a_file.non')
    create_file(source_directory, 'a_file_2.hlp')
    result = scanner.misc_extensions_in(source_directory)
    extensions = sorted(['.non', '.hlp'])

    assert sorted(list(result)) == extensions


def test_media_extensions_includes_upper_and_lower_case_extensions():
    media_exts = ['.bmp', '.gif', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic',
     '.BMP', '.GIF', '.JPG', '.JPEG', '.PNG', '.TIF', '.TIFF', '.HEIC',
     '.mp4', '.mov', '.avi', '.wmv', '.mkv', '.hevc',
     '.MP4', '.MOV', '.AVI', '.WMV', '.MKV', '.HEVC']
    assert sorted(MEDIA_EXTENSIONS) == sorted(media_exts)
