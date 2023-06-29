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


def test_creates_year_and_quarter_target_directories():
    assert not os.path.isdir(target_directory)

    generator.prepare_target_path(static_source_directory, target_root_directory, 'test_file.txt')

    assert os.path.isdir(target_directory)


def test_creates_quarter_target_directory_if_year_directory_already_exists():
    desired_target_dir_year = target_root_directory + '2023/'

    assert not os.path.isdir(desired_target_dir_year)

    create_directory(desired_target_dir_year)
    generator.prepare_target_path(static_source_directory, target_root_directory, 'test_file.txt')

    assert os.path.isdir(target_directory)


def test_adds_suffix_to_filename_if_there_is_a_name_clash_with_existing_file():
    filename = 'file_1.txt'
    create_file_with_data(target_directory, filename, 'Some original data')

    path = generator.prepare_target_path(static_source_directory, target_root_directory, filename)

    assert path == target_directory + 'file_1___1.txt'


def test_increments_number_suffix_if_name_clashes_with_file_with_suffix():
    filename = 'a_file___1.jpeg'
    create_file_with_data(target_directory, filename, 'Some original data')

    path = generator.prepare_target_path(static_source_directory, target_root_directory, filename)

    assert path == target_directory + 'a_file___2.jpeg'


def test_returns_empty_path_if_generated_path_points_to_file_with_identical_name_suffix_and_size():
    filename = 'this_file.txt'
    create_file_with_data(target_directory, 'this_file.txt', 'Unique data')
    create_file_with_data(target_directory, 'this_file___1.txt', 'Same data')

    path = generator.prepare_target_path(static_source_directory, target_root_directory, filename)

    assert path == ''

