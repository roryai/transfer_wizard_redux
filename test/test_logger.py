from app.logger import Logger
from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_init_log_file_creates_file():
    logger = Logger(destination_root_directory)
    assert os.path.exists(logger.log_file_path)

    timestamp_format = '%Y-%m-%d-%H%M.%S'
    expected_filename = datetime.now().strftime(timestamp_format) + 'media_transfer_logfile.txt'
    assert os.path.basename(logger.log_file_path) == expected_filename


def test_successful_write_to_logfile():
    logger = Logger(destination_root_directory)
    source_file_path = 'test_source.txt'
    destination_filepath = '/destination' + source_file_path
    logger.log_successful_copy(source_file_path, destination_filepath)

    with open(logger.log_file_path, 'r') as file:
        content = file.read()

    expected_entry = f'Copy succeeded: {source_file_path} copied to {destination_filepath}\n'
    assert expected_entry == content


def test_unsuccessful_write_to_logfile():
    logger = Logger(destination_root_directory)
    source_file_path = 'test_source.txt'
    destination_filepath = '/destination' + source_file_path
    logger.log_unsuccessful_copy(source_file_path, destination_filepath)

    with open(logger.log_file_path, 'r') as file:
        content = file.read()

    expected_entry = f'Copy failed:    {source_file_path} not copied to {destination_filepath}\n'
    assert expected_entry == content
