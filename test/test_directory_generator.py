import pytest

from .test_helpers import *
from app.directory_generator import DirectoryGenerator

generator = DirectoryGenerator()


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_generates_path_including_year_and_quarter():
    filename = 'test_file.txt'
    source_filepath = static_source_directory + filename
    generated_path = generator.prepare_target_path(source_filepath, target_root_directory, filename)

    assert generated_path == target_directory + filename


def test_adds_suffix_to_filename_if_there_is_a_name_clash_with_existing_file():
    filename = 'file_1.txt'
    source_filepath = static_source_directory + filename

    create_file_with_data(target_directory, filename, 'Some original data')

    path = generator.prepare_target_path(source_filepath, target_root_directory, filename)

    assert path == target_directory + 'file_1___1.txt'


def test_increments_number_suffix_if_name_clashes_with_file_with_suffix():
    filename = 'a_file___1.jpeg'
    source_filepath = static_source_directory + filename

    create_file_with_data(target_directory, filename, 'Some original data')

    path = generator.prepare_target_path(source_filepath, target_root_directory, filename)

    assert path == target_directory + 'a_file___2.jpeg'


def test_returns_empty_path_if_generated_path_points_to_file_with_identical_name_suffix_and_size():
    filename = 'this_file.txt'
    source_filepath = static_source_directory + filename

    create_file_with_data(target_directory, filename, 'Unique data')
    create_file_with_data(target_directory, 'this_file___1.txt', 'Same data')

    path = generator.prepare_target_path(source_filepath, target_root_directory, filename)

    assert path == ''

