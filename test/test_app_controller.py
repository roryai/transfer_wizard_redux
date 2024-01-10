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


def test_copies_file_to_generated_directory(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    filename = 'file.jpeg'
    create_file_with_data(source_directory, filename, 'datum')
    source_filepath = source_directory + filename

    destination_directory = get_destination_directory(source_filepath)
    destination_filepath = destination_directory + filename

    assert not Path(destination_directory).is_dir()
    assert not Path(destination_filepath).is_file()

    copy_files()

    assert Path(destination_filepath).is_file()
    assert open(destination_filepath).read() == 'datum'


def test_does_not_copy_duplicate_file(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    filename = 'file.jpeg'
    create_file_with_data(source_directory, filename, 'datum')
    source_filepath = source_directory + filename

    destination_directory = get_destination_directory(source_filepath)
    destination_filepath = destination_directory + filename
    # create an identical file in the destination directory:
    # the candidate file will not be copied; the existing file will not be overwritten
    create_file_with_data(destination_directory, filename, 'datum')
    existing_file_mtime_pre_run = Path(destination_filepath).stat().st_mtime

    copy_files()

    existing_file_mtime_post_run = Path(destination_filepath).stat().st_mtime

    assert Path(destination_filepath).is_file()
    assert open(destination_filepath).read() == 'datum'
    assert existing_file_mtime_post_run == existing_file_mtime_pre_run


def test_copies_file_to_generated_directory_when_name_clashes_with_existing_file(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')

    filename = 'file.jpeg'
    create_file_with_data(source_directory, filename, 'datum')
    source_filepath = source_directory + filename

    destination_directory = get_destination_directory(source_filepath)
    # create a file with same name as candidate file but with different data
    name_clash_file = create_file_with_data(destination_directory, filename, 'DATA')

    # the candidate file will have a suffix added because of the name clash
    filename_with_suffix = 'file___1.jpeg'
    destination_filepath = destination_directory + filename_with_suffix

    existing_file_mtime_pre_run = Path(name_clash_file).stat().st_mtime

    copy_files()

    existing_file_mtime_post_run = Path(name_clash_file).stat().st_mtime

    assert Path(destination_filepath).is_file()
    assert open(destination_filepath).read() == 'datum'
    assert Path(name_clash_file).is_file()
    assert open(name_clash_file).read() == 'DATA'
    assert existing_file_mtime_post_run == existing_file_mtime_pre_run
