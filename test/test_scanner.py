import pytest

from .test_helpers import *
from app.scanner import Scanner

scanner = Scanner(source_dir, target_dir)


@pytest.fixture(autouse=True)
def run_before_tests():
    delete_files_in(source_dir)
    delete_files_in(target_dir)
    yield


def test_scanner_discovers_files_to_be_transferred():
    create_desired_files()

    files_to_transfer = scanner.scan_dirs()

    assert sorted(files_to_transfer) == sorted(desired_source_filepath_list())


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

    assert sorted(files_to_transfer) == sorted(desired_source_filepath_list())
