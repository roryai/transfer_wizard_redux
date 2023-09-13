from app.app_controller import AppController
from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_copies_file_to_generated_directory(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    filename = 'file.jpeg'
    create_file_with_data(dynamic_source_directory, filename, 'datum')
    source_filepath = dynamic_source_directory + filename

    target_directory = target_root_directory + determine_year_and_quarter(source_filepath)
    target_filepath = target_directory + filename

    assert not Path(target_directory).is_dir()
    assert not Path(target_filepath).is_file()

    AppController(dynamic_source_directory, target_root_directory).run()

    assert Path(target_filepath).is_file()
    assert open(target_filepath).read() == 'datum'


def test_does_not_copy_duplicate_file(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')

    filename = 'file.jpeg'
    create_file_with_data(dynamic_source_directory, filename, 'datum')
    source_filepath = dynamic_source_directory + filename

    target_directory = target_root_directory + determine_year_and_quarter(source_filepath)
    target_filepath = target_directory + filename
    create_file_with_data(target_directory, filename, 'datum')
    existing_file_mtime_pre_run = os.stat(target_filepath).st_mtime

    AppController(dynamic_source_directory, target_root_directory).run()

    existing_file_mtime_post_run = os.stat(target_filepath).st_mtime

    assert Path(target_filepath).is_file()
    assert open(target_filepath).read() == 'datum'
    assert existing_file_mtime_post_run == existing_file_mtime_pre_run


def test_copies_file_to_generated_directory_when_name_clashes_with_existing_file(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')

    filename = 'file.jpeg'
    create_file_with_data(dynamic_source_directory, filename, 'datum')
    source_filepath = dynamic_source_directory + filename

    target_directory = target_root_directory + determine_year_and_quarter(source_filepath)
    # create a file with same name but different contents
    name_clash_file = create_file_with_data(target_directory, filename, 'DATA')

    target_filename = 'file___1.jpeg'
    target_filepath = target_directory + target_filename

    AppController(dynamic_source_directory, target_root_directory).run()

    assert Path(target_filepath).is_file()
    assert open(target_filepath).read() == 'datum'
    assert Path(name_clash_file).is_file()
    assert open(name_clash_file).read() == 'DATA'
