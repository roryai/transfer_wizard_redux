from .helpers import *

from app.file_factory import FileFactory


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()
    clear_database()


def save_pre_copy_file_record(source_filepath):
    FileFactory(source_filepath, destination_root_directory).save_pre_copy_file_record()


def setup_and_run_test_class(filename='test_file.jpeg', run_func=True,
                             source_data='default_source_data', dest_data='default_dest_data'):
    func = create_file_with_data
    source_filepath = func(source_directory, filename, source_data)
    destination_directory = static_destination_path(source_filepath)
    func(destination_directory, filename, dest_data) if run_func else None
    save_pre_copy_file_record(source_filepath)
    return filename, source_filepath, destination_directory


def test_a_file_is_built_and_saved():
    source_data = 'this_string_is_23_bytes'
    filename, source_filepath, destination_directory = setup_and_run_test_class(
        source_data=source_data, run_func=False)

    file = instantiate_file_from_db_record()

    assert file.source_filepath == source_filepath
    assert file.destination_filepath == destination_directory + filename
    assert file.size == 23
    assert file.name_clash is False
    assert file.copied is None
    assert file.media is True


def test_file_is_marked_as_having_name_clash_when_an_existing_destination_file_has_same_name_and_different_size():
    _, source_filepath, destination_directory = setup_and_run_test_class(
        source_data='original data', dest_data='different data')

    file = instantiate_file_from_db_record()
    expected_filename = 'test_file___1.jpeg'

    assert file.source_filepath == source_filepath
    assert file.destination_filepath == destination_directory + expected_filename
    assert file.size == 13
    assert file.name_clash is True


def test_duplicate_files_are_marked_as_having_no_destination_filepath_and_not_having_name_clash():
    data = 'same data'
    _, source_filepath, destination_directory = setup_and_run_test_class(
        source_data=data, dest_data=data)

    file = instantiate_file_from_db_record()

    assert file.source_filepath == source_filepath
    assert file.name_clash is False
    assert file.destination_filepath is None
