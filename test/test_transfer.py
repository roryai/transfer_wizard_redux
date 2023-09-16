from app.transfer import Transfer

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    clear_test_directories()


def test_transfers_provided_file():
    assert filenames_in_directory(target_root_directory) == []
    source_filepath = create_file(source_directory, 'a_file.jpeg')

    Transfer().copy_files(source_filepath, target_root_directory)

    assert p(source_filepath).is_file()
