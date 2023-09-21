from app.file import File
from app.file_builder import FileBuilder
from app.transfer import Transfer

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    clear_test_directories()
    clear_database()


def test_transfers_file():
    assert filenames_in_directory(target_root_directory) == []
    source_filepath = create_file(source_directory, 'a_file.jpeg')
    target_filepath = get_target_path(source_filepath, target_root_directory)
    FileBuilder(source_filepath, target_root_directory).build()

    Transfer().copy_files()

    assert p(target_filepath).is_file()


def test_transfers_multiple_files():
    assert filenames_in_directory(target_root_directory) == []
    source_filepath_1 = create_file(source_directory, 'a_file1.jpeg')
    source_filepath_2 = create_file(source_directory, 'a_file2.jpeg')
    source_filepath_3 = create_file(source_directory, 'a_file3.jpeg')
    FileBuilder(source_filepath_1, target_root_directory).build()
    FileBuilder(source_filepath_2, target_root_directory).build()
    FileBuilder(source_filepath_3, target_root_directory).build()

    target_filepath_1 = get_target_path(source_filepath_1, target_root_directory)
    target_filepath_2 = get_target_path(source_filepath_2, target_root_directory)
    target_filepath_3 = get_target_path(source_filepath_3, target_root_directory)

    Transfer().copy_files()

    assert p(target_filepath_1).is_file()
    assert p(target_filepath_2).is_file()
    assert p(target_filepath_3).is_file()


def test_marks_file_as_transferred_upon_successful_transfer():
    gateway = FileGateway()
    source_filepath = create_file(source_directory, 'a_file.jpeg')
    target_filepath = get_target_path(source_filepath, target_root_directory)
    FileBuilder(source_filepath, target_root_directory).build()

    Transfer().copy_files()

    assert p(target_filepath).is_file()

    file = File.init_from_record(gateway.select_all()[0])

    assert file.copied is True
