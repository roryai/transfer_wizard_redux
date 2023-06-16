import os

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
    create_desired_source_files()

    source_files = desired_source_filepaths()
    Transfer().copy_files(source_files, target_dir)

    assert filenames_in_directory(target_dir) == filenames_in_directory(source_dir)


def test_does_not_copy_file_if_duplicate_already_exists():
    source_filepath = source_dir + 'a_file.jpeg'
    existing_target_filepath = target_dir + 'a_file.jpeg'
    open(source_filepath, 'x').close()
    open(existing_target_filepath, 'x').close()
    existing_file_mod_time_pre_copy = os.stat(existing_target_filepath).st_mtime
    source_files = [source_filepath]
    Transfer().copy_files(source_files, target_dir)

    existing_file_mod_time_post_copy = os.stat(existing_target_filepath).st_mtime

    assert existing_file_mod_time_post_copy == existing_file_mod_time_pre_copy


def test_adds_suffix_to_copied_file_if_name_clashes_with_existing_file():
    create_desired_source_files()
    existing_filepath = target_dir + 'a_file.jpeg'
    same_name_different_contents = open(existing_filepath, 'x')
    same_name_different_contents.write('Some original data')
    same_name_different_contents.close()
    source_files = desired_source_filepaths()
    Transfer().copy_files(source_files, target_dir)

    assert os.path.isfile(target_dir + 'a_file___1.jpeg')


def test_increments_number_suffix_if_already_exists():
    filename = 'a_file___1.jpeg'
    open(source_dir + filename, 'x').close()
    same_name_different_contents = open(target_dir + filename, 'x')
    same_name_different_contents.write('Some original data')
    same_name_different_contents.close()
    source_files = [source_dir + filename]
    Transfer().copy_files(source_files, target_dir)

    assert os.path.isfile(target_dir + 'a_file___2.jpeg')


def test_increments_duplicate_number_suffix_until_unused_path_discovered():
    source_file_path = create_file_with_data(source_dir, 'a_file.jpeg', 'Some original data')
    create_file_with_data(target_dir, 'a_file.jpeg', 'Some very original data')
    create_file_with_data(target_dir, 'a_file___1.jpeg', 'Mostly original data')

    Transfer().copy_files([source_file_path], target_dir)

    assert os.path.isfile(target_dir + 'a_file___2.jpeg')


def test_skips_file_if_incremented_identical_file_discovered():
    pass
