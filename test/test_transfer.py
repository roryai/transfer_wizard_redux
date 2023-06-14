import pytest

from app.transfer import Transfer
from .test_helpers import *


@pytest.fixture(autouse=True)
def run_before_tests():
    delete_files_in(source_dir)
    delete_files_in(target_dir)
    yield


def test_desired_files_are_transferred():
    assert filenames_in_directory(target_dir) == []
    create_desired_files()

    source_files = desired_source_filepath_list()
    Transfer().copy_files(source_files, target_dir)

    assert filenames_in_directory(target_dir) == filenames_in_directory(source_dir)

def test_does_not_copy_files_if_file_already_exists():
    create_desired_files()
    existing_filepath = target_dir + 'a_file.jpeg'
    open(existing_filepath, 'x').close()
    existing_file_mod_time_pre_copy = os.stat(existing_filepath).st_mtime
    source_files = desired_source_filepath_list()
    Transfer().copy_files(source_files, target_dir)

    existing_file_mod_time_post_copy = os.stat(existing_filepath).st_mtime

    assert existing_file_mod_time_post_copy == existing_file_mod_time_pre_copy

