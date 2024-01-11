from app.app_controller import AppController
from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()
    clear_database()


def copy_files():
    AppController(destination_directory=destination_root_directory,
                  source_directory=source_directory).copy_files_from_source_to_destination()


def create_source_file(filename='file.jpeg'):
    source_filepath = create_file_with_data(source_directory, filename, 'datum')
    destination_directory = static_destination_path(source_filepath)
    destination_filepath = destination_directory + filename
    return filename, destination_directory, destination_filepath


def test_copies_file_to_destination_directory(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    filename, destination_directory, destination_filepath = create_source_file()

    assert not Path(destination_directory).is_dir()
    assert not Path(destination_filepath).is_file()

    copy_files()

    assert Path(destination_filepath).is_file()
    assert open(destination_filepath).read() == 'datum'


def test_does_not_copy_duplicate_file(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    filename, destination_directory, destination_filepath = create_source_file()
    # create an identical file in the destination directory:
    # the candidate file will not be copied; the existing file will not be overwritten
    create_file_with_data(destination_directory, filename, 'datum')
    existing_file_mtime_pre_run = Path(destination_filepath).stat().st_mtime

    copy_files()

    existing_file_mtime_post_run = Path(destination_filepath).stat().st_mtime

    assert Path(destination_filepath).is_file()
    assert open(destination_filepath).read() == 'datum'
    assert existing_file_mtime_post_run == existing_file_mtime_pre_run


def test_copies_file_with_suffix_added_when_name_clashes_with_existing_file(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    filename, destination_directory, _ = create_source_file()
    # create a file with same name as source file but with different data
    existing_file_with_identical_name = create_file_with_data(destination_directory, filename, 'DATA')

    # the source file will have a suffix added because of the name clash
    generated_filename_for_source_file = 'file___1.jpeg'
    expected_sourcefile_destination_path = destination_directory + generated_filename_for_source_file

    existing_file_mtime_pre_run = Path(existing_file_with_identical_name).stat().st_mtime

    copy_files()

    existing_file_mtime_post_run = Path(existing_file_with_identical_name).stat().st_mtime

    assert Path(expected_sourcefile_destination_path).is_file()
    assert open(expected_sourcefile_destination_path).read() == 'datum'
    assert Path(existing_file_with_identical_name).is_file()
    assert open(existing_file_with_identical_name).read() == 'DATA'
    assert existing_file_mtime_pre_run == existing_file_mtime_post_run
