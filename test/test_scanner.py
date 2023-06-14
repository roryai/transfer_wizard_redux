import os

import pytest

from app.scanner import Scanner

source_dir = "/Users/rory/code/transfer_wizard_redux/test/media/source/"
target_dir = "/Users/rory/code/transfer_wizard_redux/test/media/target/"

DESIRED_PHOTO_EXTENSIONS = ['.bmp', '.gif', '.jpg', '.jpeg', '.png', '.tif', '.tiff']

scanner = Scanner(source_dir, target_dir)


def desired_file_list():
    files = []
    for ext in DESIRED_PHOTO_EXTENSIONS:  # TODO use list comprehension here
        files.append(source_dir + 'a_file' + ext)
    return files


def create_desired_files():
    for file_path in desired_file_list():
        open(file_path, 'x').close()


def delete_files_in(directory):
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))


@pytest.fixture(autouse=True)
def run_before_tests():
    delete_files_in(source_dir)
    delete_files_in(target_dir)
    yield


def test_scanner_discovers_files_to_be_transferred():
    create_desired_files()

    files_to_transfer = scanner.scan_dirs()

    assert sorted(files_to_transfer) == sorted(desired_file_list())


def test_scanner_ignores_files_without_desired_extensions():
    create_desired_files()
    undesired_files = [
        source_dir + "sales.zip",
        source_dir + "sales.rar",
        source_dir + "sales.bin",
        ]
    for file in undesired_files:
        open(file, 'x').close()

    files_to_transfer = scanner.scan_dirs()

    assert sorted(files_to_transfer) == sorted(desired_file_list())
