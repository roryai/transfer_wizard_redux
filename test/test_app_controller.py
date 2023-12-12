from app.app_controller import AppController
from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()
    clear_database()


def test_copies_file_to_generated_directory(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    filename = 'file.jpeg'
    create_file_with_data(source_directory, filename, 'datum')
    source_filepath = source_directory + filename

    destination_directory = get_destination_directory(source_filepath)
    destination_filepath = destination_directory + filename

    assert not p(destination_directory).is_dir()
    assert not p(destination_filepath).is_file()

    AppController(source_directory, destination_root_directory).run()

    assert p(destination_filepath).is_file()
    assert open(destination_filepath).read() == 'datum'


def test_does_not_copy_duplicate_file(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    filename = 'file.jpeg'
    create_file_with_data(source_directory, filename, 'datum')
    source_filepath = source_directory + filename

    destination_directory = get_destination_directory(source_filepath)
    destination_filepath = destination_directory + filename
    create_file_with_data(destination_directory, filename, 'datum')
    existing_file_mtime_pre_run = p(destination_filepath).stat().st_mtime

    AppController(source_directory, destination_root_directory).run()

    existing_file_mtime_post_run = p(destination_filepath).stat().st_mtime

    assert p(destination_filepath).is_file()
    assert open(destination_filepath).read() == 'datum'
    assert existing_file_mtime_post_run == existing_file_mtime_pre_run


def test_copies_file_to_generated_directory_when_name_clashes_with_existing_file(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')

    filename = 'file.jpeg'
    create_file_with_data(source_directory, filename, 'datum')
    source_filepath = source_directory + filename

    destination_directory = get_destination_directory(source_filepath)
    # create a file with same name but different contents
    name_clash_file = create_file_with_data(destination_directory, filename, 'DATA')

    destination_filename = 'file___1.jpeg'
    destination_filepath = destination_directory + destination_filename

    AppController(source_directory, destination_root_directory).run()

    assert p(destination_filepath).is_file()
    assert open(destination_filepath).read() == 'datum'
    assert p(name_clash_file).is_file()
    assert open(name_clash_file).read() == 'DATA'
