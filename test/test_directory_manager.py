from app.directory_manager import DirectoryManager

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_creates_year_and_quarter_target_directories():
    target_directory = target_root_directory + '2023/Q2/'
    assert not p(target_directory).is_dir()

    DirectoryManager().create_directory_if_not_exists(target_directory)

    assert p(target_directory).is_dir()


def test_creates_quarter_target_directory_if_year_directory_already_exists():
    target_directory_year = target_root_directory + '2023/'
    target_directory_quarter = target_directory_year + 'Q2/'

    assert not p(target_directory_year).is_dir()

    create_directory(target_directory_year)

    assert not p(target_directory_quarter).is_dir()

    DirectoryManager().create_directory_if_not_exists(target_directory_quarter)

    assert p(target_directory_quarter).is_dir()


def test_files_in_existing_directory_persist_after_second_call_to_create_directory():
    filename = 'test_file.jpeg'
    source_filepath = create_file(source_directory, filename)
    target_directory = target_root_directory + determine_year_and_quarter(source_filepath)
    target_filepath = target_directory + filename

    DirectoryManager().create_directory_if_not_exists(target_directory)
    shutil.copy2(source_filepath, target_filepath)
    DirectoryManager().create_directory_if_not_exists(target_directory)

    assert p(target_directory + filename).is_file()


def test_raises_error_if_directory_does_not_exist():
    with pytest.raises(FileNotFoundError):
        DirectoryManager().check_if_directory_exists(target_root_directory + 'jgjgjg')
