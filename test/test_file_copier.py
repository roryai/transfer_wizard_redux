from app.file import File
from app.file_factory import FileFactory
from app.file_copier import FileCopier

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    clear_test_directories()
    clear_database()


def test_copies_file():
    assert filenames_in_directory(destination_root_directory) == []
    source_filepath = create_file(source_directory, 'a_file.jpeg')
    destination_filepath = get_destination_path(source_filepath)
    FileFactory(source_filepath, destination_root_directory).save_pre_copy_file_record()

    FileCopier().copy_source_files_to_destination_directory()

    assert p(destination_filepath).is_file()


def test_copies_multiple_files():
    assert filenames_in_directory(destination_root_directory) == []
    source_filepath_1 = create_file(source_directory, 'a_file1.jpeg')
    source_filepath_2 = create_file(source_directory, 'a_file2.jpeg')
    source_filepath_3 = create_file(source_directory, 'a_file3.jpeg')
    FileFactory(source_filepath_1, destination_root_directory).save_pre_copy_file_record()
    FileFactory(source_filepath_2, destination_root_directory).save_pre_copy_file_record()
    FileFactory(source_filepath_3, destination_root_directory).save_pre_copy_file_record()

    destination_filepath_1 = get_destination_path(source_filepath_1)
    destination_filepath_2 = get_destination_path(source_filepath_2)
    destination_filepath_3 = get_destination_path(source_filepath_3)

    FileCopier().copy_source_files_to_destination_directory()

    assert p(destination_filepath_1).is_file()
    assert p(destination_filepath_2).is_file()
    assert p(destination_filepath_3).is_file()


def test_marks_file_as_copied_upon_successful_copy():
    gateway = FileGateway()
    source_filepath = create_file(source_directory, 'a_file.jpeg')
    destination_filepath = get_destination_path(source_filepath)
    FileFactory(source_filepath, destination_root_directory).save_pre_copy_file_record()

    FileCopier().copy_source_files_to_destination_directory()

    assert p(destination_filepath).is_file()

    file = File.init_from_record(gateway.select_all()[0])

    assert file.copied is True


def test_copies_files_that_are_marked_as_having_name_clash():
    shared_filename = 'a_file.jpeg'
    source_filepath = create_file(source_directory, shared_filename)
    destination_directory = get_destination_directory(source_filepath)
    create_file_with_data(destination_directory, shared_filename, 'Some data')
    assert filenames_in_directory(destination_directory) == [shared_filename]
    FileFactory(source_filepath, destination_root_directory).save_pre_copy_file_record()
    FileCopier().copy_source_files_to_destination_directory()

    assert filenames_in_directory(destination_directory) == [shared_filename, 'a_file___1.jpeg']
