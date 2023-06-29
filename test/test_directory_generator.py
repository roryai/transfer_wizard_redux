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
    source_filepath = source_directory + filename
    desired_target_path = target_root_directory + '2023/Q2/' + filename
    generated_path = generator.prepare_target_path(source_filepath, target_root_directory, filename)
    assert generated_path == desired_target_path


def test_creates_year_and_quarter_target_directories():
    desired_target_dir = target_directory

    assert not os.path.isdir(desired_target_dir)

    generator.prepare_target_path(source_directory, target_root_directory, 'test_file.txt')

    assert os.path.isdir(desired_target_dir)


def test_creates_quarter_target_directory_if_year_directory_already_exists():
    desired_target_dir_year = target_root_directory + '2023/'
    desired_target_dir_quarter = target_directory

    assert not os.path.isdir(desired_target_dir_year)

    create_directory(desired_target_dir_year)

    generator.prepare_target_path(source_directory, target_root_directory, 'test_file.txt')

    assert os.path.isdir(desired_target_dir_quarter)


def test_adds_suffix_to_filename_if_there_is_a_name_clash_with_existing_file():
    filename = 'file_1.txt'
    target_filepath = create_file_with_data(target_directory, filename, 'Some original data')

    path = generator.prepare_target_path(source_directory, target_root_directory, filename)

    assert path == target_directory + 'file_1___1.txt'
    delete_file(target_filepath)


def test_increments_number_suffix_if_name_clashes_with_file_with_suffix():
    filename = 'a_file___1.jpeg'
    target_filepath = create_file_with_data(target_directory, filename, 'Some original data')

    path = generator.prepare_target_path(source_directory, target_root_directory, filename)

    assert path == target_directory + 'a_file___2.jpeg'
    delete_file(target_filepath)


def test_returns_empty_path_if_generated_path_points_to_file_with_identical_name_suffix_and_size():
    filename = 'this_file.txt'
    file1 = create_file_with_data(target_directory, 'this_file.txt', 'Unique data')
    file2 = create_file_with_data(target_directory, 'this_file___1.txt', 'Same data')

    path = generator.prepare_target_path(source_directory, target_root_directory, filename)

    assert path == ''
    delete_file(file1)
    delete_file(file2)

