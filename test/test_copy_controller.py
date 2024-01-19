from app.copy_controller import CopyController
from .helpers import pytest, Path, cleanup, construct_path, create_test_media_files, \
    create_test_misc_files, destination_root_directory, source_directory


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
    def test_copies_media_file_to_destination_directory(self, monkeypatch_user_input_yes):
        _, _, destination_directory, destination_filepath = create_test_media_files()
        
        copy_files(include_misc_files=True)

        assert Path(destination_filepath).is_file()
        assert open(destination_filepath).read() == 'default_source_data'

    def test_copies_misc_file_to_destination_directory(self, monkeypatch_user_input_yes):
        _, _, destination_directory, destination_filepath = create_test_misc_files()

        copy_files(include_misc_files=True)

        assert Path(destination_filepath).is_file()
        assert open(destination_filepath).read() == 'default_source_data'


class TestExcludeMiscFiles:
    def test_copies_media_file_to_destination_directory(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda: 'y')
        _, _, destination_directory, destination_filepath = create_test_media_files()

        copy_files(include_misc_files=False)

        assert Path(destination_filepath).is_file()
        assert open(destination_filepath).read() == 'default_source_data'

    def test_does_not_copy_misc_file_or_create_destination_directory(self, monkeypatch_user_input_yes):
        _, _, destination_directory, destination_filepath = create_test_misc_files()

        copy_files(include_misc_files=False)

        assert not Path(destination_directory).is_dir()
        assert not Path(destination_filepath).is_file()


class TestSharedExamples:
    def test_does_not_copy_file_when_user_enters_char_other_than_y(self, monkeypatch_user_input_yes):
        _, _, destination_directory, destination_filepath = create_test_misc_files()

        copy_files(include_misc_files=False)

        assert not Path(destination_directory).is_dir()
        assert not Path(destination_filepath).is_file()

    def test_does_not_copy_duplicate_file(self, monkeypatch_user_input_yes):
        data = 'identical_data'
        filename, _, destination_directory, destination_filepath = create_test_media_files(
            source_data=data, dest_data=data, create_destination_file=True)

        existing_file_mtime_pre_run = Path(destination_filepath).stat().st_mtime

        copy_files(include_misc_files=True)

        existing_file_mtime_post_run = Path(destination_filepath).stat().st_mtime

        assert Path(destination_filepath).is_file()
        assert open(destination_filepath).read() == data
        assert existing_file_mtime_post_run == existing_file_mtime_pre_run

    def test_copies_file_with_suffix_added_when_name_clashes_with_existing_file(self, monkeypatch_user_input_yes):
        filename, _, destination_directory, existing_file_with_identical_name = create_test_media_files(
            create_destination_file=True)

        generated_filename_for_source_file = 'test_media_file___1.jpeg'
        expected_sourcefile_destination_path = construct_path(destination_directory, generated_filename_for_source_file)

        existing_file_mtime_pre_run = Path(existing_file_with_identical_name).stat().st_mtime

        copy_files(include_misc_files=True)

        existing_file_mtime_post_run = Path(existing_file_with_identical_name).stat().st_mtime

        assert Path(expected_sourcefile_destination_path).is_file()
        assert open(expected_sourcefile_destination_path).read() == 'default_source_data'
        assert Path(existing_file_with_identical_name).is_file()
        assert open(existing_file_with_identical_name).read() == 'default_destination_data'
        assert existing_file_mtime_pre_run == existing_file_mtime_post_run
