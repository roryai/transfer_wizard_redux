from .helpers import *

from app.file import File
from app.file_factory import FileFactory


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()
    clear_database()


def test_a_file_is_built_and_saved():
    filename = 'a_file.jpeg'
    source_filepath = create_file(source_directory, filename)
    FileFactory(source_filepath, destination_root_directory).save_pre_copy_file_record()
    destination_directory = get_destination_directory(source_filepath)

    record = FileGateway().select_all()[0]
    file = File.init_from_record(record)

    assert file.source_filepath == source_filepath
    assert file.destination_filepath == destination_directory + filename
    assert file.size == 0
    assert file.name_clash is False


def test_a_file_has_name_clash_when_existing_destination_file_has_same_name_and_different_size():
    filename = 'a_file.jpeg'
    source_filepath = create_file_with_data(source_directory, filename, 'original data')
    destination_directory = get_destination_directory(source_filepath)
    create_file_with_data(destination_directory, filename, 'different data')

    FileFactory(source_filepath, destination_root_directory).save_pre_copy_file_record()

    record = FileGateway().select_all()[0]
    file = File.init_from_record(record)
    expected_filename = 'a_file___1.jpeg'

    assert file.source_filepath == source_filepath
    assert file.destination_filepath == destination_directory + expected_filename
    assert file.size == 13
    assert file.name_clash is True


def test_duplicate_files_are_marked_as_not_having_name_clash():
    filename = 'a_file.jpeg'
    source_filepath = create_file_with_data(source_directory, filename, 'same data')
    destination_directory = get_destination_directory(source_filepath)
    create_file_with_data(destination_directory, filename, 'same data')

    FileFactory(source_filepath, destination_root_directory).save_pre_copy_file_record()

    record = FileGateway().select_all()[0]
    file = File.init_from_record(record)

    assert file.name_clash is False
