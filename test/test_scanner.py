import os

import pytest

from app.scanner import Scanner

source_dir = "/Users/rory/code/transfer_wizard_redux/test/media/source/"
target_dir = "/Users/rory/code/transfer_wizard_redux/test/media/target/"

scanner = Scanner(source_dir, target_dir)


def delete_files_in(directory):
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))


@pytest.fixture(autouse=True)
def run_before_tests():
    delete_files_in(source_dir)
    delete_files_in(target_dir)
    yield


def test_scanner_discovers_files_to_be_transferred():
    file_path = source_dir + "desired.jpeg"
    open(file_path, 'x').close()

    files_to_transfer = scanner.scan_dirs()

    assert files_to_transfer == [file_path]


def test_scanner_ignores_files_without_desired_extensions():
    desired_file = source_dir + "desired.jpeg"
    undesired_files = [
        source_dir + "sales.jpg",
        source_dir + "sales.rar",
        source_dir + "sales.gif",
        ]
    open(desired_file, 'x').close()
    for file in undesired_files:
        open(file, 'x').close()

    files_to_transfer = scanner.scan_dirs()

    assert files_to_transfer == [desired_file]
