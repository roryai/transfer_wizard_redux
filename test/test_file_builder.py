from .helpers import *

from app.file import File
from app.file_builder import FileBuilder


@pytest.fixture(autouse=True)
def teardown():
    clear_database()
    clear_test_directories()


def test_a_file_is_built_and_saved():
    filename = 'a_file.jpeg'
    source_filepath = create_file(source_directory, filename)
    FileBuilder(source_filepath, target_root_directory).build()
    target_directory = target_root_directory + determine_year_and_quarter(source_filepath)

    record = FileGateway().select_all()[0]
    file = File.init_from_record(record)

    assert file.source_filepath == source_filepath
    assert file.target_filepath == target_directory + filename
    assert file.size == 0
    assert file.name_clash is False


def test_a_file_has_name_clash_when_existing_target_file_has_same_name_and_different_size():
    filename = 'a_file.jpeg'
    source_filepath = create_file_with_data(source_directory, filename, 'original data')
    target_directory = target_root_directory + determine_year_and_quarter(source_filepath)
    create_file_with_data(target_directory, filename, 'different data')

    FileBuilder(source_filepath, target_root_directory).build()

    record = FileGateway().select_all()[0]
    file = File.init_from_record(record)
    expected_filename = 'a_file___1.jpeg'

    assert file.source_filepath == source_filepath
    assert file.target_filepath == target_directory + expected_filename
    assert file.size == 13
    assert file.name_clash is True