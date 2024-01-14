from app.directory_manager import DirectoryManager

from .helpers import pytest, Path, shutil, clear_db_and_test_directories, create_file_on_disk, construct_path, destination_root_directory, source_directory, static_destination_path


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_db_and_test_directories()


def test_creates_a_directory():
    destination_directory = construct_path(destination_root_directory, '2023')
    assert not Path(destination_directory).is_dir()

    DirectoryManager().create_directory_if_not_exists(destination_directory)

    assert Path(destination_directory).is_dir()


def test_files_in_existing_directory_persist_after_second_call_to_create_directory():
    filename = 'test_file.jpeg'
    source_filepath = create_file_on_disk(source_directory, filename)
    destination_directory = static_destination_path(source_filepath)
    destination_filepath = construct_path(destination_directory, filename)

    DirectoryManager().create_directory_if_not_exists(destination_directory)

    assert not Path(destination_filepath).is_file()

    shutil.copy2(source_filepath, destination_filepath)

    assert Path(destination_filepath).is_file()

    DirectoryManager().create_directory_if_not_exists(destination_directory)

    assert Path(destination_filepath).is_file()


def test_raises_error_if_directory_does_not_exist():
    fake_directory = f'{destination_root_directory}fake'
    with pytest.raises(FileNotFoundError, match=f'{fake_directory} is not a valid directory.'):
        DirectoryManager().check_if_directory_exists(fake_directory)
