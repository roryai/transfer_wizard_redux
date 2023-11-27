from app.file import File
from app.file_factory import FileFactory
from app.file_copier import FileCopier

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    clear_test_directories()
    clear_database()


def test_copies_file():
    assert filenames_in_directory(target_root_directory) == []
    source_filepath = create_file(source_directory, 'a_file.jpeg')
    target_filepath = get_target_path(source_filepath)
    FileFactory(source_filepath, target_root_directory).save_pre_copy_file_record()

    FileCopier().copy_source_files_to_target_directory()

    assert p(target_filepath).is_file()


def test_copies_multiple_files():
    assert filenames_in_directory(target_root_directory) == []
    source_filepath_1 = create_file(source_directory, 'a_file1.jpeg')
    source_filepath_2 = create_file(source_directory, 'a_file2.jpeg')
    source_filepath_3 = create_file(source_directory, 'a_file3.jpeg')
    FileFactory(source_filepath_1, target_root_directory).save_pre_copy_file_record()
    FileFactory(source_filepath_2, target_root_directory).save_pre_copy_file_record()
    FileFactory(source_filepath_3, target_root_directory).save_pre_copy_file_record()

    target_filepath_1 = get_target_path(source_filepath_1)
    target_filepath_2 = get_target_path(source_filepath_2)
    target_filepath_3 = get_target_path(source_filepath_3)

    FileCopier().copy_source_files_to_target_directory()

    assert p(target_filepath_1).is_file()
    assert p(target_filepath_2).is_file()
    assert p(target_filepath_3).is_file()


def test_marks_file_as_copied_upon_successful_copy():
    gateway = FileGateway()
    source_filepath = create_file(source_directory, 'a_file.jpeg')
    target_filepath = get_target_path(source_filepath)
    FileFactory(source_filepath, target_root_directory).save_pre_copy_file_record()

    FileCopier().copy_source_files_to_target_directory()

    assert p(target_filepath).is_file()

    file = File.init_from_record(gateway.select_all()[0])

    assert file.copied is True


def test_copies_files_that_are_marked_as_having_name_clash():
    shared_filename = 'a_file.jpeg'
    source_filepath = create_file(source_directory, shared_filename)
    target_directory = get_target_directory(source_filepath)
    create_file_with_data(target_directory, shared_filename, 'Some data')
    assert filenames_in_directory(target_directory) == [shared_filename]
    FileFactory(source_filepath, target_root_directory).save_pre_copy_file_record()
    FileCopier().copy_source_files_to_target_directory()

    assert filenames_in_directory(target_directory) == [shared_filename, 'a_file___1.jpeg']
