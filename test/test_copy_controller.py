from app.copy_controller import CopyController
from .helpers import (pytest, Path, cleanup, construct_path, create_test_misc_files, destination_root_directory,
                      prepare_test_media_source_file, prepare_test_media_destination_duplicate_file,
                      prepare_test_media_destination_name_clash_file, image_with_metadata_destination_directory,
                      source_directory)


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


@pytest.fixture
def monkeypatch_user_input_yes(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')


def copy_files():
    CopyController(destination_root_directory, source_directory).copy_files()


def test_copies_media_file_to_destination_directory(monkeypatch_user_input_yes):
    destination_filepath = prepare_test_media_source_file()

    copy_files()

    assert Path(destination_filepath).is_file()
    assert Path(destination_filepath).stat().st_size == 195514


def test_does_not_copy_file_when_user_enters_char_other_than_y(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'z')
    _, _, destination_directory, destination_filepath = create_test_misc_files()

    copy_files()

    assert not Path(destination_directory).is_dir()
    assert not Path(destination_filepath).is_file()


def test_does_not_copy_duplicate_file(monkeypatch_user_input_yes):
    destination_filepath = prepare_test_media_source_file()
    prepare_test_media_destination_duplicate_file()

    existing_file_mtime_pre_run = Path(destination_filepath).stat().st_mtime

    copy_files()

    existing_file_mtime_post_run = Path(destination_filepath).stat().st_mtime

    assert Path(destination_filepath).is_file()
    assert Path(destination_filepath).stat().st_size == 195514
    assert existing_file_mtime_post_run == existing_file_mtime_pre_run


def test_copies_file_with_suffix_added_when_name_clashes_with_existing_file(monkeypatch_user_input_yes):
    prepare_test_media_source_file()
    existing_file_with_identical_name = prepare_test_media_destination_name_clash_file()
    expected_destination_path = construct_path(image_with_metadata_destination_directory,
                                               'IMG_1687_68E3___1.JPG')

    existing_file_mtime_pre_run = Path(existing_file_with_identical_name).stat().st_mtime

    copy_files()

    existing_file_mtime_post_run = Path(existing_file_with_identical_name).stat().st_mtime

    assert Path(expected_destination_path).is_file()
    assert Path(existing_file_with_identical_name).is_file()
    assert existing_file_mtime_pre_run == existing_file_mtime_post_run
