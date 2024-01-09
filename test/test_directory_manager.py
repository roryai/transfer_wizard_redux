from app.directory_manager import DirectoryManager

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    clear_test_directories()


def test_creates_year_and_quarter_destination_directories():
    destination_directory = destination_root_directory + '2023/Q2/'
    assert not Path(destination_directory).is_dir()

    DirectoryManager().create_directory_if_not_exists(destination_directory)

    assert Path(destination_directory).is_dir()


def test_creates_quarter_destination_directory_if_year_directory_already_exists():
    destination_directory_year = destination_root_directory + '2023/'
    destination_directory_quarter = destination_directory_year + 'Q2/'

    assert not Path(destination_directory_year).is_dir()

    create_directory(destination_directory_year)

    assert not Path(destination_directory_quarter).is_dir()

    DirectoryManager().create_directory_if_not_exists(destination_directory_quarter)

    assert Path(destination_directory_quarter).is_dir()


def test_files_in_existing_directory_persist_after_second_call_to_create_directory():
    filename = 'test_file.jpeg'
    source_filepath = create_file(source_directory, filename)
    destination_directory = get_destination_directory(source_filepath)
    destination_filepath = destination_directory + filename

    DirectoryManager().create_directory_if_not_exists(destination_directory)
    shutil.copy2(source_filepath, destination_filepath)
    DirectoryManager().create_directory_if_not_exists(destination_directory)

    assert Path(destination_directory + filename).is_file()


def test_raises_error_if_directory_does_not_exist():
    with pytest.raises(FileNotFoundError):
        DirectoryManager().check_if_directory_exists(destination_root_directory + 'jgjgjg')
