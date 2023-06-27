import pytest

from .test_helpers import *
from app.scanner import Scanner

scanner = Scanner()


@pytest.fixture(autouse=True)
def run_before_tests():
    delete_files_in(source_dir)
    delete_files_in(target_dir)
    yield


def test_scanner_discovers_files_to_be_transferred():
    create_desired_source_files()

    files_to_transfer = scanner.scan_dirs(source_dir)

    assert files_to_transfer == desired_source_filepaths()


def test_scanner_ignores_files_without_desired_extensions():
    create_desired_source_files()
    undesired_files = [
        source_dir + "sales.zip",
        source_dir + "sales.rar",
        source_dir + "sales.bin",
        ]
    for file in undesired_files:
        open(file, 'x').close()

    files_to_transfer = scanner.scan_dirs(source_dir)

    assert files_to_transfer == desired_source_filepaths()
