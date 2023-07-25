import os
from pathlib import Path
import shutil

from app.scanner import VALID_PHOTO_EXTENSIONS

test_directory = str(Path(__file__).parent)
test_media_directory = test_directory + '/media/'
static_source_directory = test_media_directory + 'static_source/'
dynamic_source_directory = test_media_directory + 'dynamic_source/'
target_root_directory = test_media_directory + 'target/'
target_directory = target_root_directory + '2023/Q2/'


def create_valid_files():
    for file_path in valid_source_filepaths():
        open(file_path, 'x').close()


def valid_source_filepaths():
    files = []
    for ext in VALID_PHOTO_EXTENSIONS:
        files.append(dynamic_source_directory + 'a_file' + ext)
    return sorted(files)


def clear_test_directories():
    paths = [dynamic_source_directory, target_root_directory]
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
    Path(directory_path).mkdir(parents=True, exist_ok=True)
