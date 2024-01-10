from .helpers import *

from app.file_factory import FileFactory


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()
    clear_database()


def save_pre_copy_file_record(source_filepath):
    FileFactory(source_filepath, destination_root_directory).save_pre_copy_file_record()


def test_a_file_is_built_and_saved():
    filename = 'a_file.jpeg'
    source_filepath = create_file(source_directory, filename)

    save_pre_copy_file_record(source_filepath)

    destination_directory = get_destination_directory(source_filepath)
    file = instantiate_file_from_db_record()

    assert file.source_filepath == source_filepath
    assert file.destination_filepath == destination_directory + filename
    assert file.size == 0
    assert file.name_clash is False
    assert file.copied is None
    assert file.media is True


def test_file_is_marked_as_having_name_clash_when_an_existing_destination_file_has_same_name_and_different_size():
    filename = 'a_file.jpeg'
    source_filepath = create_file_with_data(source_directory, filename, 'original data')
    destination_directory = get_destination_directory(source_filepath)
    create_file_with_data(destination_directory, filename, 'different data')

    save_pre_copy_file_record(source_filepath)

    file = instantiate_file_from_db_record()
    expected_filename = 'a_file___1.jpeg'

    assert file.source_filepath == source_filepath
    assert file.destination_filepath == destination_directory + expected_filename
    assert file.size == 13
    assert file.name_clash is True


def test_duplicate_files_are_marked_as_having_no_destination_filepath_and_not_having_name_clash():
    filename = 'a_file.jpeg'
    source_filepath = create_file_with_data(source_directory, filename, 'same data')
    destination_directory = get_destination_directory(source_filepath)
    create_file_with_data(destination_directory, filename, 'same data')

    save_pre_copy_file_record(source_filepath)

    file = instantiate_file_from_db_record()

    assert file.source_filepath == source_filepath
    assert file.name_clash is False
    assert file.destination_filepath is None
