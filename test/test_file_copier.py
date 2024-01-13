from .helpers import (pytest, Path, clear_db_and_test_directories, construct_path,
                      create_file_on_disk, file_instance, instantiate_file_from_db_record,
                      source_directory)
from app.file_copier import FileCopier


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_db_and_test_directories()


def copy_source_files_to_destination():
    FileCopier().copy_source_files_to_destination()


def filename_and_destination_filepath(filename='filename.jpeg'):
    destination_filepath = construct_path(source_directory, filename)
    return filename, destination_filepath


def create_source_file_and_save_file_record(filename='filename.jpeg'):
    source_filepath = construct_path(source_directory, filename)
    create_file_on_disk(source_directory, filename)
    file = file_instance(source_filepath=source_filepath)
    file.save()
    return file


def test_copies_single_file():
    _, destination_filepath = filename_and_destination_filepath()

    assert not Path(destination_filepath).is_file()

    create_source_file_and_save_file_record()
    copy_source_files_to_destination()

    assert Path(destination_filepath).is_file()


def test_copies_multiple_files():
    _, destination_filepath_1 = filename_and_destination_filepath()
    filename_2, destination_filepath_2 = filename_and_destination_filepath('a_file2.jpeg')

    assert not Path(destination_filepath_1).is_file()
    assert not Path(destination_filepath_2).is_file()

    file_1 = create_source_file_and_save_file_record()
    file_2 = create_source_file_and_save_file_record(filename_2)

    copy_source_files_to_destination()

    assert Path(file_1.destination_filepath).is_file()
    assert Path(file_2.destination_filepath).is_file()


def test_records_a_successful_copy_attempt():
    file = create_source_file_and_save_file_record()

    copy_source_files_to_destination()

    retrieved_file = instantiate_file_from_db_record(file.source_filepath)

    assert retrieved_file.copied is True
    assert retrieved_file.copy_attempted is True


def test_records_an_unsuccessful_copy_attempt(monkeypatch):
    def mock_is_file(_):
        return False

    # this approach isn't ideal, but it runs the section of code under test
    monkeypatch.setattr(Path, "is_file", mock_is_file)

    file = create_source_file_and_save_file_record()

    copy_source_files_to_destination()

    retrieved_file = instantiate_file_from_db_record(file.source_filepath)

    assert retrieved_file.copied is False
    assert retrieved_file.copy_attempted is True
