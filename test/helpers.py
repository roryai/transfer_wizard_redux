import os
from pathlib import Path
import pytest
import shutil

from main import ROOT_DIR
from app.db_initializer import DBInitializer
from app.file import File
from app.file_gateway import FileGateway
from app.logger import Logger, LoggerMeta


def construct_path(*args):
    return os.path.join(*args)


test_directory = str(Path(__file__).parent)
test_resources_directory = construct_path(test_directory, 'test_resources')
source_directory = construct_path(test_resources_directory, 'source')
static_media_directory = construct_path(test_resources_directory, 'static_media')
logfile_directory = construct_path(test_directory, 'logs')
destination_root_directory = construct_path(test_resources_directory, 'destination')
misc_destination_root_directory = construct_path(destination_root_directory, 'misc')
misc_destination_year_directory = construct_path(misc_destination_root_directory, '2023')
media_destination_year_directory = construct_path(destination_root_directory, '2023/Q4')
metadata_error_destination_year_directory = construct_path(destination_root_directory, 'error/2023/Q4')
default_source_media_filepath = construct_path(source_directory, 'test_media_file.jpeg')
default_destination_media_filepath = construct_path(media_destination_year_directory, 'test_media_file.jpeg')
image_with_metadata_filename = 'IMG_1687_68E3.jpg'
image_with_metadata_source_filepath = os.path.join(static_media_directory, image_with_metadata_filename)
image_with_metadata_destination_directory = os.path.join(destination_root_directory, '2018/Q3')

DBInitializer(ROOT_DIR).init_test_database()
Logger().init_log_file(logfile_directory)


def file_instance(source_filepath=default_source_media_filepath,
                  destination_filepath=default_destination_media_filepath,
                  size=1024, copied=False, name_clash=False, media=True,
                  copy_attempted=False):
    return File(source_filepath=source_filepath, destination_filepath=destination_filepath,
                size=size, copied=copied, name_clash=name_clash, media=media,
                copy_attempted=copy_attempted)


def create_test_media_files(filename='test_media_file.jpeg', create_destination_file=False,
                            source_data='default_source_data', dest_data='default_destination_data'):
    source_filepath = create_file_on_disk_with_data(source_directory, filename, source_data)
    set_file_creation_time(source_filepath)
    destination_filepath = construct_path(media_destination_year_directory, filename)
    create_file_on_disk_with_data(media_destination_year_directory, filename,
                                  dest_data) if create_destination_file else None
    return filename, source_filepath, media_destination_year_directory, destination_filepath


def create_test_misc_files(filename='test_misc_file.gif', create_destination_file=False,
                           source_data='default_source_data', dest_data='default_destination_data'):
    source_filepath = create_file_on_disk_with_data(source_directory, filename, source_data)
    set_file_creation_time(source_filepath)
    destination_filepath = construct_path(misc_destination_year_directory, filename)
    create_file_on_disk_with_data(misc_destination_year_directory, filename, dest_data) \
        if create_destination_file else None
    return filename, source_filepath, misc_destination_year_directory, destination_filepath


def prepare_test_media_source_file(directory=source_directory):
    Path(directory).mkdir(parents=True, exist_ok=True)
    shutil.copy2(image_with_metadata_source_filepath, directory)
    return os.path.join(image_with_metadata_destination_directory, image_with_metadata_filename)


def prepare_test_media_destination_name_clash_file():
    destination_filepath = os.path.join(image_with_metadata_destination_directory, 'IMG_1687_68E3.jpg')
    Path(image_with_metadata_destination_directory).mkdir(parents=True, exist_ok=True)
    open(destination_filepath, 'x').close()
    return destination_filepath


def prepare_test_media_destination_duplicate_file():
    Path(image_with_metadata_destination_directory).mkdir(parents=True, exist_ok=True)
    shutil.copy2(image_with_metadata_source_filepath, image_with_metadata_destination_directory)
    return os.path.join(image_with_metadata_destination_directory, 'IMG_1687_68E3.jpg')


def set_file_creation_time(filepath):
    time_in_past = 1701639908  # 03/12/23
    # setting mtime to before creation time sets both to that time
    os.utime(filepath, (time_in_past, time_in_past))


def create_file_on_disk(directory, filename):
    return create_file_on_disk_with_data(directory, filename)


def create_file_on_disk_with_data(directory_path, filename, data=''):
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    file_path = construct_path(directory_path, filename)
    with open(file_path, 'x') as file:
        file.write(data)
    return file_path


def insert_db_record(file):
    FileGateway().insert(file)


def instantiate_file_from_db_record(source_filepath):
    gateway = FileGateway()
    return File.init_from_record(gateway.select(source_filepath))


def clear_database():
    FileGateway().wipe_database()


def clear_test_directories():
    paths = [source_directory, destination_root_directory, logfile_directory]
    for path in paths:
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(construct_path(root, f))
            for d in dirs:
                shutil.rmtree(construct_path(root, d))


def cleanup():
    LoggerMeta._instance = {}
    Logger().init_log_file(logfile_directory)
    clear_database()
    clear_test_directories()
