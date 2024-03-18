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


def copy_files(include_misc_files):
    CopyController(destination_root_directory=destination_root_directory,
                   source_root_directory=source_directory,
                   include_misc_files=include_misc_files).copy_files()


class TestIncludeMiscFiles:
    def test_copies_media_file_to_destination_directory(self, mocker, monkeypatch_user_input_yes):
        destination_filepath = prepare_test_media_source_file()

        copy_files(include_misc_files=True)

        assert Path(destination_filepath).is_file()
        assert Path(destination_filepath).stat().st_size == 195514

    def test_copies_misc_file_to_destination_directory(self, mocker, monkeypatch_user_input_yes):
        _, _, destination_directory, destination_filepath = create_test_misc_files()

        copy_files(include_misc_files=True)

        assert Path(destination_filepath).is_file()
        assert open(destination_filepath).read() == 'default_source_data'


class TestExcludeMiscFiles:
    def test_copies_media_file_to_destination_directory(self, mocker, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda: 'y')
        destination_filepath = prepare_test_media_source_file()

        copy_files(include_misc_files=False)

        assert Path(destination_filepath).is_file()
        assert Path(destination_filepath).stat().st_size == 195514

    def test_does_not_copy_misc_file_or_create_destination_directory(self, mocker, monkeypatch_user_input_yes):
        _, _, destination_directory, destination_filepath = create_test_misc_files()

        copy_files(include_misc_files=False)

        assert not Path(destination_directory).is_dir()
        assert not Path(destination_filepath).is_file()


class TestSharedExamples:
    def test_does_not_copy_file_when_user_enters_char_other_than_y(self, mocker, monkeypatch_user_input_yes):
        _, _, destination_directory, destination_filepath = create_test_misc_files()

        copy_files(include_misc_files=False)

        assert not Path(destination_directory).is_dir()
        assert not Path(destination_filepath).is_file()

    def test_does_not_copy_duplicate_file(self, mocker, monkeypatch_user_input_yes):
        destination_filepath = prepare_test_media_source_file()
        prepare_test_media_destination_duplicate_file()

        existing_file_mtime_pre_run = Path(destination_filepath).stat().st_mtime

        copy_files(include_misc_files=True)

        existing_file_mtime_post_run = Path(destination_filepath).stat().st_mtime

        assert Path(destination_filepath).is_file()
        assert Path(destination_filepath).stat().st_size == 195514
        assert existing_file_mtime_post_run == existing_file_mtime_pre_run

    def test_copies_file_with_suffix_added_when_name_clashes_with_existing_file(self, mocker,
                                                                                monkeypatch_user_input_yes):
        prepare_test_media_source_file()
        existing_file_with_identical_name = prepare_test_media_destination_name_clash_file()
        expected_destination_path = construct_path(image_with_metadata_destination_directory,
                                                   'IMG_1687_68E3___1.JPG')

        existing_file_mtime_pre_run = Path(existing_file_with_identical_name).stat().st_mtime

        copy_files(include_misc_files=True)

        existing_file_mtime_post_run = Path(existing_file_with_identical_name).stat().st_mtime

        assert Path(expected_destination_path).is_file()
        assert Path(existing_file_with_identical_name).is_file()
        assert existing_file_mtime_pre_run == existing_file_mtime_post_run
