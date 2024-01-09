from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_init_log_file_creates_file():
    # assign singleton Logger (created in .helpers) so that it can be deleted and then reinitialised
    logger = Logger()
    del logger
    Logger().init_log_file(logfile_directory)

    assert os.path.exists(Logger().log_file_path)

    timestamp_format = '%Y-%m-%d-%H%M.%S'
    expected_filename = datetime.now().strftime(timestamp_format) + 'media_transfer_logfile.txt'
    assert os.path.basename(Logger().log_file_path) == expected_filename


def test_successful_write_to_logfile():
    source_file_path = 'test_source.txt'
    destination_filepath = '/destination' + source_file_path
    Logger().log_successful_copy(source_file_path, destination_filepath)

    with open(Logger().log_file_path, 'r') as file:
        content = file.read()

    expected_entry = f'Copy succeeded: {source_file_path} copied to {destination_filepath}\n'
    assert expected_entry == content


def test_unsuccessful_write_to_logfile():
    source_file_path = 'test_source.txt'
    destination_filepath = '/destination' + source_file_path
    Logger().log_unsuccessful_copy(source_file_path, destination_filepath)

    with open(Logger().log_file_path, 'r') as file:
        content = file.read()

    expected_entry = f'Copy failed:    {source_file_path} not copied to {destination_filepath}\n'
    assert expected_entry == content


def test_logs_error():
    # reset error log as it may be populated by other tests
    Logger().error_messages = []

    values = ['/source/file1.jpg', '/destination/file1.jpg', 1024, None, False]
    error = 'UNIQUE constraint failed: files.source_filepath'
    expected_error_message = "Error: UNIQUE constraint failed: files.source_filepath. Values: " \
                             "['/source/file1.jpg', '/destination/file1.jpg', 1024, None, False]"
    Logger().log_error(error, values)
    assert Logger().error_messages[0] == expected_error_message


def test_writes_errors_to_logfile():
    # reset error log as it may be populated by other tests
    Logger().error_messages = []

    values = ['/source/file1.jpg', '/destination/file1.jpg', 1024, None, False]
    error = 'UNIQUE constraint failed: files.source_filepath'
    Logger().log_error(error, values)
    Logger().write_errors_to_logfile()

    with open(Logger().log_file_path, 'r') as file:
        content = file.read()

    expected_content = "\nErrors:\nError: UNIQUE constraint failed: files.source_filepath. Values: " \
                       "['/source/file1.jpg', '/destination/file1.jpg', 1024, None, False]\n"

    assert expected_content == content
