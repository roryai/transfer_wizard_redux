from .helpers import *
from pathlib import PosixPath

gateway = FileGateway()


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_database()
    clear_test_directories()


def test_files_can_be_compared():
    file = file_instance()
    file_2 = file_instance()

    assert file == file_2


def test_file_instantiated_from_record_has_expected_attributes():
    file_instance().save()

    retrieved_file = instantiate_file_from_db_record()

    assert retrieved_file.source_filepath == default_source_filepath
    assert retrieved_file.destination_filepath == default_destination_filepath
    assert retrieved_file.size == 1024
    assert retrieved_file.name_clash is False
    assert retrieved_file.copied is False
    assert retrieved_file.media is True
    assert retrieved_file.copy_attempted is False
    assert len(retrieved_file.__dict__) == 7


def test_determines_file_directory():
    destination_directory = file_instance(destination_filepath='/destination/filename.jpeg'
                                          ).destination_directory()
    assert destination_directory == PosixPath('/destination')
