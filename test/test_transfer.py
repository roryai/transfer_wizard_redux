import os

import pytest

from app.transfer import Transfer
from .test_helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_desired_files_are_transferred():
    assert filenames_in_directory(target_root_directory) == []
    create_desired_source_files()

    source_files = desired_source_filepaths()
    Transfer().copy_files(source_files, target_root_directory)

    assert filenames_in_directory(target_directory) == filenames_in_directory(temp_source_directory)


