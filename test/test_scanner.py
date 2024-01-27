from .helpers import (pytest, Path, cleanup, create_file_on_disk,
                      construct_path, source_directory)
from app.scanner import Scanner

scanner = Scanner()


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def test_discovers_a_media_file():
    media_filepath = create_file_on_disk(source_directory, 'file.jpg')

    discovered_filepaths = list(scanner.media_filepaths_in(source_directory))

    assert discovered_filepaths == [media_filepath]


def test_discovers_a_misc_file():
    misc_filepath = create_file_on_disk(source_directory, 'file.gif')

    discovered_extensions = list(scanner.misc_filepaths_in(source_directory))

    assert discovered_extensions == [misc_filepath]


def test_discovers_a_file_in_a_nested_directory():
    nested_directory = construct_path(source_directory, 'nested')
    Path(nested_directory).mkdir(parents=True, exist_ok=True)
    misc_filepath = create_file_on_disk(nested_directory, 'file.gif')

    discovered_extensions = list(scanner.misc_filepaths_in(source_directory))

    assert discovered_extensions == [misc_filepath]


def test_discovers_a_file_in_a_twice_nested_directory():
    nested_directory = construct_path(source_directory, 'nest')
    inside_nested_directory = construct_path(source_directory, 'egg')
    Path(nested_directory).mkdir(parents=True, exist_ok=True)
    Path(inside_nested_directory).mkdir(parents=True, exist_ok=True)
    misc_filepath = create_file_on_disk(inside_nested_directory, 'file.gif')

    discovered_extensions = list(scanner.misc_filepaths_in(source_directory))

    assert discovered_extensions == [misc_filepath]


def test_discovers_a_misc_extension():
    create_file_on_disk(source_directory, 'file.txt')

    discovered_extensions = list(scanner.misc_extensions_in(source_directory))

    assert discovered_extensions == ['.txt']


def test_ignores_files_with_misc_extensions_when_scanning_for_media_files():
    create_file_on_disk(source_directory, 'file.txt')

    discovered_filepaths = list(scanner.media_filepaths_in(source_directory))

    assert len(discovered_filepaths) == 0


def test_ignores_files_with_media_extensions_when_scanning_for_misc_files():
    create_file_on_disk(source_directory, 'a_file.jpg')
    discovered_extensions = list(scanner.misc_filepaths_in(source_directory))

    assert len(discovered_extensions) == 0


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


def test_discovers_a_file_with_an_upper_case_photo_file():
    media_filepath = create_file_on_disk(source_directory, 'file.JPG')

    discovered_filepaths = list(scanner.media_filepaths_in(source_directory))

    assert discovered_filepaths == [media_filepath]


def test_discovers_a_file_with_an_upper_case_video_file():
    media_filepath = create_file_on_disk(source_directory, 'file.MOV')

    discovered_filepaths = list(scanner.media_filepaths_in(source_directory))

    assert discovered_filepaths == [media_filepath]


def test_discovers_a_file_with_an_upper_case_misc_file():
    media_filepath = create_file_on_disk(source_directory, 'file.TXT')

    discovered_filepaths = list(scanner.misc_filepaths_in(source_directory))

    assert discovered_filepaths == [media_filepath]
