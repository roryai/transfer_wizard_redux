from datetime import datetime
from .helpers import *

from app.logger import LoggerMeta


@pytest.fixture(autouse=True)
def teardown():
    LoggerMeta._instance = {}
    Logger().init_log_file(logfile_directory)
    yield
    clear_test_directories()


def file_content():
    with open(Logger().log_file_path, 'r') as file:
        return file.read()


values = ['/source/file1.jpg', '/destination/file1.jpg', 1024, None, False]
error = 'UNIQUE constraint failed: files.source_filepath'
source_file_path = 'source/test_source.txt'
destination_filepath = construct_path('/destination', source_file_path)


def test_init_log_file_creates_file():
    assert os.path.exists(Logger().log_file_path)

    timestamp_format = '%Y-%m-%d-%H%M.%S'
    expected_filename = datetime.now().strftime(timestamp_format) + '_media_transfer_logfile.txt'

    assert Path(Logger().log_file_path).name == expected_filename


def test_successful_write_to_logfile():
    Logger().log_successful_copy(source_file_path, destination_filepath)

    expected_entry = f'Copy succeeded: {source_file_path} copied to {destination_filepath}\n'

    assert expected_entry == file_content()


def test_unsuccessful_write_to_logfile():
    Logger().log_unsuccessful_copy(source_file_path, destination_filepath)

    expected_entry = f'Copy failed:    {source_file_path} not copied to {destination_filepath}\n'

    assert expected_entry == file_content()


def test_logs_error():
    expected_error_message = "Error: UNIQUE constraint failed: files.source_filepath. Values: " \
                             "['/source/file1.jpg', '/destination/file1.jpg', 1024, None, False]"
    Logger().log_error(error, values)

    assert Logger().error_messages[0] == expected_error_message
    assert len(Logger().error_messages) == 1


def test_writes_errors_to_logfile():
    expected_content = "\nErrors:\nError: UNIQUE constraint failed: files.source_filepath. Values: " \
                       "['/source/file1.jpg', '/destination/file1.jpg', 1024, None, False]\n"

    Logger().log_error(error, values)
    Logger().write_errors_to_logfile()

    assert expected_content == file_content()
