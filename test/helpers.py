import os
from pathlib import Path
import pytest
import shutil

from app.db_initializer import DBInitializer
from app.file import File
from app.file_gateway import FileGateway
from app.logger import Logger

test_directory = str(Path(__file__).parent)
test_media_directory = test_directory + '/media/'
source_directory = test_media_directory + 'source/'
logfile_directory = test_directory + '/logs'
destination_root_directory = test_media_directory + 'destination/'

DBInitializer().init_test_database()
Logger().init_log_file(logfile_directory)


def file_instance(source_filepath=source_directory + 'filename.jpg',
                  destination_filepath=destination_root_directory + 'filename.jpg',
                  size=1024, copied=None, name_clash=False, media=True):
    return File(source_filepath=source_filepath, destination_filepath=destination_filepath,
                size=size, copied=copied, name_clash=name_clash, media=media)


def create_test_files(filename='test_file.jpeg', create_destination_file=False,
                      source_data='default_source_data', dest_data='default_destination_data'):
    source_filepath = create_file_with_data(source_directory, filename, source_data)
    destination_directory = static_destination_path(source_filepath)
    destination_filepath = destination_directory + filename  # os join
    create_file_with_data(destination_directory, filename, dest_data) if create_destination_file else None
    return filename, source_filepath, destination_directory, destination_filepath


def static_destination_path(source_filepath):
    time_in_past = 1701639908  # 03/12/23
    # setting mtime to before creation time sets both to that time
    os.utime(source_filepath, (time_in_past, time_in_past))
    return os.path.join(destination_root_directory, '2023/Q4/')


def create_file_with_data(directory_path, filename, data=''):
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(directory_path, filename)
    file = open(file_path, 'x')
    file.write(data)
    file.close()
    return file_path


def create_file(directory, filename):
    return create_file_with_data(directory, filename)


def filenames_in(directory):
    files = []
    for (_, _, filenames) in os.walk(directory):
        files.extend(filenames)
        break
    return sorted(files)


def insert_db_record(file):
    FileGateway().insert(file)


def instantiate_file_from_db_record():
    gateway = FileGateway()
    assert gateway.count() == 1
    return File.init_from_record(gateway.select_all()[0])


def clear_database():
    FileGateway().wipe_database()


def clear_test_directories():
    paths = [source_directory, destination_root_directory, logfile_directory]
    for path in paths:
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
