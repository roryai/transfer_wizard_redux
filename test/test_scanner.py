import pytest

from .test_helpers import *
from app.scanner import Scanner

scanner = Scanner()


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_scanner_discovers_files_to_be_transferred():
    create_desired_source_files()

    files_to_transfer = scanner.scan_dirs(dynamic_source_directory)

    assert files_to_transfer == desired_source_filepaths()


def test_scanner_ignores_files_without_desired_extensions():
    create_desired_source_files()
    undesired_files = [
        dynamic_source_directory + "sales.zip",
        dynamic_source_directory + "sales.rar",
        dynamic_source_directory + "sales.bin",
        ]
    for file in undesired_files:
        open(file, 'x').close()

    files_to_transfer = scanner.scan_dirs(dynamic_source_directory)

    assert files_to_transfer == desired_source_filepaths()
