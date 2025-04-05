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


def ignores_non_media_file_extension():
    create_file_on_disk(source_directory, 'file.gif')

    discovered_filepaths = list(scanner.media_filepaths_in(source_directory))

    assert discovered_filepaths == []


def test_discovers_multiple_media_files():
    jpg_path = create_file_on_disk(source_directory, 'file.jpg')
    mov_path = create_file_on_disk(source_directory, 'file.mov')
    raf_path = create_file_on_disk(source_directory, 'file.raf')

    discovered_filepaths = list(scanner.media_filepaths_in(source_directory))

    assert sorted(discovered_filepaths) == sorted([jpg_path, mov_path, raf_path])


def test_discovers_a_file_in_a_nested_directory():
    nested_directory = construct_path(source_directory, 'nested')
    Path(nested_directory).mkdir(parents=True, exist_ok=True)
    misc_filepath = create_file_on_disk(nested_directory, 'file.mov')

    discovered_extensions = list(scanner.media_filepaths_in(source_directory))

    assert discovered_extensions == [misc_filepath]


def test_discovers_a_file_in_a_twice_nested_directory():
    nested_directory = construct_path(source_directory, 'nest')
    inside_nested_directory = construct_path(source_directory, 'egg')
    Path(nested_directory).mkdir(parents=True, exist_ok=True)
    Path(inside_nested_directory).mkdir(parents=True, exist_ok=True)
    misc_filepath = create_file_on_disk(inside_nested_directory, 'file.raf')

    discovered_extensions = list(scanner.media_filepaths_in(source_directory))

    assert discovered_extensions == [misc_filepath]


def test_discovers_an_upper_case_jpg():
    media_filepath = create_file_on_disk(source_directory, 'file.JPG')

    discovered_filepaths = list(scanner.media_filepaths_in(source_directory))

    assert discovered_filepaths == [media_filepath]


def test_discovers_an_upper_case_mov():
    media_filepath = create_file_on_disk(source_directory, 'file.MOV')

    discovered_filepaths = list(scanner.media_filepaths_in(source_directory))

    assert discovered_filepaths == [media_filepath]


def test_discovers_an_upper_case_raf():
    media_filepath = create_file_on_disk(source_directory, 'file.RAF')

    discovered_filepaths = list(scanner.media_filepaths_in(source_directory))

    assert discovered_filepaths == [media_filepath]
