from app.transfer import Transfer
from .test_helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_transfers_provided_file():
    assert filenames_in_directory(target_root_directory) == []
    file_path = static_source_directory + 'file_1.txt'

    Transfer().copy_files([file_path], target_root_directory)

    assert os.path.isfile(file_path)
