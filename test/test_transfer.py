from app.file import File
from app.transfer import Transfer

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    clear_test_directories()


def test_transfers_file():
    assert filenames_in_directory(target_root_directory) == []
    source_filepath = create_file(source_directory, 'a_file.jpeg')

    Transfer().copy_files()

    assert p(source_filepath).is_file()


def test_marks_file_as_transferred_upon_successful_transfer():
    gateway = FileGateway()
    source_filepath = create_file(source_directory, 'a_file.jpeg')

    Transfer().copy_files()

    assert p(source_filepath).is_file()

    file = File.init_from_record(gateway.select_all()[0])

    assert file.copied is True
