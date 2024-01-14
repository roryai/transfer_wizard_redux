from .helpers import pytest, clear_db_and_test_directories, create_file_on_disk, source_directory
from app.scanner import Scanner, MEDIA_EXTENSIONS

scanner = Scanner()


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_db_and_test_directories()


def test_discovers_a_media_file_when_scanning_for_media():
    media_filepath = create_file_on_disk(source_directory, 'file.jpg')

    discovered_filepaths = list(scanner.media_filepaths_in(source_directory))

    assert discovered_filepaths == [media_filepath]


def test_ignores_files_without_desired_extensions_when_scanning_for_media():
    create_file_on_disk(source_directory, 'file.txt')

    discovered_filepaths = list(scanner.media_filepaths_in(source_directory))

    assert len(discovered_filepaths) == 0


def test_discovers_a_misc_extension():
    create_file_on_disk(source_directory, 'file.txt')

    discovered_extensions = list(scanner.misc_extensions_in(source_directory))

    assert discovered_extensions == ['.txt']


def test_ignores_files_with_media_extensions_when_scanning_for_misc_extensions():
    create_file_on_disk(source_directory, 'a_file.jpg')
    discovered_extensions = scanner.misc_extensions_in(source_directory)

    assert len(discovered_extensions) == 0


def test_provides_a_set_of_misc_file_extensions():
    create_file_on_disk(source_directory, 'a_file.non')
    create_file_on_disk(source_directory, 'a_file_2.non')
    result = list(scanner.misc_extensions_in(source_directory))
    extension = '.non'

    assert result == [extension]


def test_provides_multiple_misc_extensions():
    create_file_on_disk(source_directory, 'a_file.non')
    create_file_on_disk(source_directory, 'a_file_2.hlp')
    results = list(scanner.misc_extensions_in(source_directory))
    extensions = ['.hlp', '.non']

    assert sorted(results) == extensions


def test_media_extensions_includes_upper_and_lower_case_extensions():
    media_exts = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic',
                  '.BMP', '.JPG', '.JPEG', '.PNG', '.TIF', '.TIFF', '.HEIC',
                  '.mp4', '.mov', '.avi', '.wmv', '.mkv', '.hevc',
                  '.MP4', '.MOV', '.AVI', '.WMV', '.MKV', '.HEVC']
    assert sorted(MEDIA_EXTENSIONS) == sorted(media_exts)
