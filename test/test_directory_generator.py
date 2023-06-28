import pytest
import shutil

from .test_helpers import *
from app.directory_generator import DirectoryGenerator

generator = DirectoryGenerator()


@pytest.fixture(autouse=True)
def run_before_tests():
    generated_target_path = target_dir + '2023'
    if os.path.isdir(generated_target_path):
        shutil.rmtree(generated_target_path)
    delete_files_in(target_dir)
    yield


def test_generates_path_including_year_and_quarter():
    filename = 'test_file.txt'
    source_filepath = permanent_source_dir + filename
    desired_target_path = target_dir + '2023/Q2/' + filename
    generated_path = generator.prepare_target_path(source_filepath, target_dir, filename)
    assert generated_path == desired_target_path


def test_creates_year_and_quarter_target_directories():
    desired_target_dir = target_dir + '2023/Q2/'

    assert not os.path.isdir(desired_target_dir)

    generator.prepare_target_path(permanent_source_dir, target_dir, 'test_file.txt')

    assert os.path.isdir(desired_target_dir)


def test_creates_quarter_target_directory_if_year_directory_already_exists():
    desired_target_dir_year = target_dir + '2023/'
    desired_target_dir_quarter = target_dir + '2023/Q2'

    assert not os.path.isdir(desired_target_dir_year)

    create_directory(desired_target_dir_year)

    generator.prepare_target_path(permanent_source_dir, target_dir, 'test_file.txt')

    assert os.path.isdir(desired_target_dir_quarter)

