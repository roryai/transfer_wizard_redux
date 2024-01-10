from app.file_copier import FileCopier

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()
    clear_database()


def copy_files():
    FileCopier().copy_source_files_to_destination()


def create_file_and_save_file_record(filename, name_clash=False):
    filepath = source_directory + filename
    file = file_instance(source_filepath=filepath, name_clash=name_clash)
    create_file(source_directory, filename)
    file.save()
    return file


def test_copies_file():
    assert filenames_in(destination_root_directory) == []

    file = create_file_and_save_file_record('filename.jpg')

    copy_files()

    assert Path(file.destination_filepath).is_file()


def test_copies_multiple_files():
    assert filenames_in(destination_root_directory) == []

    file_1 = create_file_and_save_file_record('a_file1.jpeg')
    file_2 = create_file_and_save_file_record('a_file2.jpeg')
    file_3 = create_file_and_save_file_record('a_file3.jpeg')

    copy_files()

    assert Path(file_1.destination_filepath).is_file()
    assert Path(file_2.destination_filepath).is_file()
    assert Path(file_3.destination_filepath).is_file()


def test_marks_file_as_copied_upon_successful_copy():
    gateway = FileGateway()
    file = create_file_and_save_file_record('filename.jpg')
    copy_files()

    assert Path(file.destination_filepath).is_file()

    file = instantiate_file_from_db_record()

    assert file.copied is True


def test_copies_file_that_is_marked_as_having_name_clash():
    file = create_file_and_save_file_record('filename.jpg', name_clash=True)

    copy_files()

    assert Path(file.destination_filepath).is_file()
