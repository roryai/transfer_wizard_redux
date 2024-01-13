from app.copy_controller import CopyController
from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_db_and_test_directories()


def copy_files():
    CopyController(destination_root_directory=destination_root_directory,
                   source_root_directory=source_directory).copy_media_files()


def test_copies_file_to_destination_directory(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    filename, _, destination_directory, destination_filepath = create_test_files()

    assert not Path(destination_directory).is_dir()
    assert not Path(destination_filepath).is_file()

    copy_files()

    assert Path(destination_filepath).is_file()
    assert open(destination_filepath).read() == 'default_source_data'


def test_does_not_copy_duplicate_file(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    data = 'identical_data'
    filename, _, destination_directory, destination_filepath = create_test_files(
        source_data=data, dest_data=data, create_destination_file=True)

    existing_file_mtime_pre_run = Path(destination_filepath).stat().st_mtime

    copy_files()

    existing_file_mtime_post_run = Path(destination_filepath).stat().st_mtime

    assert Path(destination_filepath).is_file()
    assert open(destination_filepath).read() == data
    assert existing_file_mtime_post_run == existing_file_mtime_pre_run


def test_copies_file_with_suffix_added_when_name_clashes_with_existing_file(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    filename, _, destination_directory, existing_file_with_identical_name = create_test_files(
        create_destination_file=True)

    generated_filename_for_source_file = 'test_file___1.jpeg'
    expected_sourcefile_destination_path = construct_path(destination_directory, generated_filename_for_source_file)

    existing_file_mtime_pre_run = Path(existing_file_with_identical_name).stat().st_mtime

    copy_files()

    existing_file_mtime_post_run = Path(existing_file_with_identical_name).stat().st_mtime

    assert Path(expected_sourcefile_destination_path).is_file()
    assert open(expected_sourcefile_destination_path).read() == 'default_source_data'
    assert Path(existing_file_with_identical_name).is_file()
    assert open(existing_file_with_identical_name).read() == 'default_destination_data'
    assert existing_file_mtime_pre_run == existing_file_mtime_post_run
