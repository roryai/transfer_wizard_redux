from datetime import datetime
import os
from pathlib import Path
import pytest
import shutil

from app.db_initializer import DBInitializer
from app.file import File
from app.file_gateway import FileGateway
from app.logger import Logger, LoggerMeta
from app.scanner import VALID_PHOTO_EXTENSIONS, VALID_VIDEO_EXTENSIONS

test_directory = str(Path(__file__).parent)
test_media_directory = test_directory + '/media/'
source_directory = test_media_directory + 'source/'
logfile_directory = test_directory + '/logs'
destination_root_directory = test_media_directory + 'destination/'

DBInitializer().init_test_database()
Logger().init_log_file(logfile_directory)


def file_instance(source_filepath=source_directory+'filename.jpg',
                  destination_filepath=destination_root_directory+'filename.jpg',
                  size=1024, copied=None, name_clash=False, media=True):
    return File(source_filepath=source_filepath, destination_filepath=destination_filepath,
                size=size, copied=copied, name_clash=name_clash, media=media)


def create_files_with_desired_extensions():
    for file_path in media_source_filepaths():
        open(file_path, 'x').close()


def create_files_without_desired_extensions():
    undesired_filenames = ["sales.zip", "sales.rar", "sales.bin"]
    for filename in undesired_filenames:
        create_file(source_directory, filename)


def instantiate_file_from_db_record():
    gateway = FileGateway()
    assert gateway.count() == 1
    return File.init_from_record(gateway.select_all()[0])


def media_source_filepaths():
    filepaths = []
    media_exts = VALID_PHOTO_EXTENSIONS + VALID_VIDEO_EXTENSIONS
    for ext in media_exts:
        filepaths.append(source_directory + 'a_file' + ext)
    return sorted(filepaths)


def clear_test_directories():
    paths = [source_directory, destination_root_directory, logfile_directory]
    for path in paths:
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))


def filenames_in(directory):
    files = []
    for (_, _, filenames) in os.walk(directory):
        files.extend(filenames)
        break
    return sorted(files)


def create_file_with_data(directory_path, filename, data=''):
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    file_path = directory_path + filename
    file = open(file_path, 'x')
    file.write(data)
    file.close()
    return file_path


def create_file(directory, filename):
    return create_file_with_data(directory, filename)


def static_destination_path(source_filepath):
    time_in_past = 1701639908  # 03/12/23
    # setting mtime to before creation time sets both to that time
    os.utime(source_filepath, (time_in_past, time_in_past))
    # destination directory path is now predictable
    return os.path.join(destination_root_directory, '2023/Q4/')


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


def insert_db_record(file):
    FileGateway().insert(file)


def reset_logger():
    LoggerMeta._instance = {}
    Logger().init_log_file(logfile_directory)
