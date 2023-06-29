import os

import pytest

from app.transfer import Transfer
from .test_helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_transfers_provided_files():
    assert filenames_in_directory(target_root_directory) == []
    create_valid_files()

    source_files = valid_source_filepaths()
    Transfer().copy_files(source_files, target_root_directory)

    assert filenames_in_directory(target_directory) == filenames_in_directory(dynamic_source_directory)
