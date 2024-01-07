from datetime import datetime
import os
from pathlib import Path as p
import pytest
import shutil

from app.db_initializer import DBInitializer
from app.file_gateway import FileGateway
from app.scanner import VALID_PHOTO_EXTENSIONS, VALID_VIDEO_EXTENSIONS

test_directory = str(p(__file__).parent)
test_media_directory = test_directory + '/media/'
source_directory = test_media_directory + 'source/'
destination_root_directory = test_media_directory + 'destination/'

DBInitializer().init_test_database()


def create_files_with_desired_extensions():
    for file_path in valid_source_filepaths():
        open(file_path, 'x').close()


def create_files_without_desired_extensions():
    undesired_filenames = ["sales.zip", "sales.rar", "sales.bin"]
    for filename in undesired_filenames:
        create_file(source_directory, filename)


def valid_source_filepaths():
    filepaths = []
    valid_exts = VALID_PHOTO_EXTENSIONS + VALID_VIDEO_EXTENSIONS
    for ext in valid_exts:
        filepaths.append(source_directory + 'a_file' + ext)
    return sorted(filepaths)


def clear_test_directories():
    paths = [source_directory, destination_root_directory]
    for path in paths:
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))


def filenames_in_directory(directory):
    files = []
    for (_, _, filenames) in os.walk(directory):
        files.extend(filenames)
        break
    return sorted(files)


def create_file_with_data(directory_path, filename, data=''):
    if not os.path.isdir(directory_path):
        create_directory(directory_path)
    file_path = directory_path + filename
    file = open(file_path, 'x')
    file.write(data)
    file.close()
    return file_path


def create_file(directory, filename):
    return create_file_with_data(directory, filename)


def create_directory(directory_path):
    p(directory_path).mkdir(parents=True, exist_ok=True)


def clear_database():
    FileGateway().wipe_database()


def get_destination_directory(source_filepath):
    return os.path.join(destination_root_directory, determine_year_and_quarter(source_filepath))


def determine_year_and_quarter(filepath):
    birthtime = datetime.fromtimestamp(os.stat(filepath).st_birthtime)
    match birthtime.month:
        case 1 | 2 | 3:
            quarter = 'Q1'
        case 4 | 5 | 6:
            quarter = 'Q2'
        case 7 | 8 | 9:
            quarter = 'Q3'
        case 10 | 11 | 12:
            quarter = 'Q4'
        case _:
            raise TypeError
    return f'{birthtime.year}/{quarter}/'


def get_destination_path(source_filepath):
    destination_dir = get_destination_directory(source_filepath)
    filename = p(source_filepath).name
    return f'{destination_dir}{filename}'


def insert_db_record(file):
    FileGateway().insert(file)


def mock_logger():
    class MockLogger:
        def __init__(self, _):
            pass

        def log_successful_copy(self, _, __):
            pass

        def log_unsuccessful_copy(self, _, __):
            pass

    return MockLogger
