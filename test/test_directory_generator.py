import pytest

from .test_helpers import *
from app.directory_generator import DirectoryGenerator

generator = DirectoryGenerator()

def test_generates_path_including_year_and_quarter():
    filename = 'test_file.txt'
    source_filepath = permanent_source_dir + filename
    desired_target_path = target_dir + '2023/Q2/' + filename
    generated_path = generator.generate_target_directory_path(source_filepath, target_dir)
    assert generated_path == desired_target_path
