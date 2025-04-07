from datetime import datetime

from .helpers import (pytest, os, Path, cleanup, construct_path,
                      logfile_directory)
from app.logger import Logger


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def file_content():
    with open(Logger().log_file_path, 'r') as file:
        return file.read()


context_message = 'Error in Class'
values = ['/source/file1.jpg', '/destination/file1.jpg', 1024, None, False]
error = 'UNIQUE constraint failed: files.source_filepath'
source_file_path = 'source/test_source.txt'
destination_filepath = construct_path('/destination', source_file_path)


def test_init_log_file_creates_file():
    Logger().init_log_file(logfile_directory)

    assert os.path.exists(Logger().log_file_path)

    timestamp_format = '%Y-%m-%d-%H%M.%S'
    expected_filename = f'{datetime.now().strftime(timestamp_format)}_media_transfer_logfile.txt'

    assert Path(Logger().log_file_path).name == expected_filename


def test_successful_write_to_logfile():
    Logger().log_successful_copy(source_file_path, destination_filepath)

    expected_entry = f'Copy succeeded: {source_file_path} copied to {destination_filepath}\n'

    assert expected_entry == file_content()
    assert Logger().successful_copy_count == 1


def test_unsuccessful_write_to_logfile():
    Logger().log_unsuccessful_copy(source_file_path, destination_filepath)

    expected_entry = f'Copy failed:    {source_file_path} not copied to {destination_filepath}\n'

    assert expected_entry == file_content()
    assert Logger().unsuccessful_copy_count == 1


def test_logs_error():
    expected_error_message = """Context: Error in Class
Error: UNIQUE constraint failed: files.source_filepath
Values: ['/source/file1.jpg', '/destination/file1.jpg', 1024, None, False]
"""
    Logger().log_error(context_message, error, values)

    assert Logger().error_messages[0] == expected_error_message
    assert len(Logger().error_messages) == 1


def test_appends_summary():
    expected_content = """
1 file copied successfully
2 files failed to copy
Errors:
Context: Error in Class
Error: UNIQUE constraint failed: files.source_filepath
Values: ['/source/file1.jpg', '/destination/file1.jpg', 1024, None, False]

"""

    Logger().successful_copy_count = 1
    Logger().unsuccessful_copy_count = 2
    Logger().log_error(context_message, error, values)
    Logger().finalise_logging()

    assert expected_content == file_content()


def test_prints_error_messages(capsys):
    expected_content = """Context: Error in Class
Error: UNIQUE constraint failed: files.source_filepath
Values: ['/source/file1.jpg', '/destination/file1.jpg', 1024, None, False]

"""

    Logger().log_error(context_message, error, values)
    Logger().finalise_logging()

    captured = capsys.readouterr()

    assert captured.out == expected_content


def test_in_console_message_when_no_errors(capsys):
    Logger().finalise_logging()

    captured = capsys.readouterr()

    assert captured.out == "No errors\n"
