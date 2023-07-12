import pytest

from .test_helpers import *
from app.directory_creator import DirectoryCreator


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_creates_year_and_quarter_target_directories():
    assert not os.path.isdir(target_directory)

    DirectoryCreator(target_directory).create_directory()

    assert os.path.isdir(target_directory)


def test_creates_quarter_target_directory_if_year_directory_already_exists():
    desired_target_dir_year = target_root_directory + '2023/'

    assert not os.path.isdir(desired_target_dir_year)

    create_directory(desired_target_dir_year)

    assert not os.path.isdir(target_directory)

    DirectoryCreator(target_directory).create_directory()

    assert os.path.isdir(target_directory)


def test_files_in_existing_directory_persist_after_call_to_create_directory():
    filename = 'test_file.txt'
    DirectoryCreator(target_directory).create_directory()
    create_file(target_directory, filename)
    DirectoryCreator(target_directory).create_directory()

    assert os.path.isfile(target_directory + filename)
