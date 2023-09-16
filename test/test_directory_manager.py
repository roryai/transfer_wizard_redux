from app.directory_manager import DirectoryManager

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_creates_year_and_quarter_target_directories():
    assert not p(target_directory).is_dir()

    DirectoryManager().create_directory_if_not_exists(target_directory)

    assert p(target_directory).is_dir()


def test_creates_quarter_target_directory_if_year_directory_already_exists():
    desired_target_dir_year = target_root_directory + '2023/'

    assert not p(desired_target_dir_year).is_dir()

    create_directory(desired_target_dir_year)

    assert not p(target_directory).is_dir()

    DirectoryManager().create_directory_if_not_exists(target_directory)

    assert p(target_directory).is_dir()


def test_files_in_existing_directory_persist_after_call_to_create_directory():
    filename = 'test_file.txt'
    DirectoryManager().create_directory_if_not_exists(target_directory)
    create_file(target_directory, filename)
    DirectoryManager().create_directory_if_not_exists(target_directory)

    assert p(target_directory + filename).is_file()


def test_raises_error_if_directory_does_not_exist():
    with pytest.raises(FileNotFoundError):
        DirectoryManager().check_if_directory_exists(target_root_directory + 'jgjgjg')
