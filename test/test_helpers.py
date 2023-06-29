import os
from pathlib import Path
import shutil

from app.scanner import PHOTO_EXTENSIONS

test_media_directory = '/Users/rory/code/transfer_wizard_redux/test/media/'
static_source_directory = test_media_directory + 'static_source/'
dynamic_source_directory = test_media_directory + 'dynamic_source/'
target_root_directory = test_media_directory + 'target/'
target_directory = target_root_directory + '2023/Q2/'


def create_valid_files():
    for file_path in valid_source_filepaths():
        open(file_path, 'x').close()


def valid_source_filepaths():
    files = []
    for ext in PHOTO_EXTENSIONS:
        files.append(dynamic_source_directory + 'a_file' + ext)
    return sorted(files)


def clear_test_directories():
    generated_target_path = target_root_directory + '2023'
    if os.path.isdir(generated_target_path):
        shutil.rmtree(generated_target_path)
    delete_files_in(dynamic_source_directory)
    delete_files_in(target_root_directory)


def delete_files_in(directory):
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))


def delete_file(filepath):
    os.remove(filepath)


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
    Path(directory_path).mkdir(parents=True, exist_ok=True)
