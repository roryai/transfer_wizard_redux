import pytest

from .test_helpers import *
from app.directory_generator import DirectoryGenerator


def test_generates_path_including_year_and_quarter():
    source_filepath = permanent_source_dir + 'test_file.txt'
    desired_target_path = "/Users/rory/code/transfer_wizard_redux/test/media/target/2023/Q2/test_file.txt"
    generated_path = DirectoryGenerator().generate_target_directory_path(source_filepath, target_dir)
    assert generated_path == desired_target_path
