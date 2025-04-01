from .helpers import (pytest, Path, cleanup, construct_path, create_file_on_disk_with_data,
                      create_test_media_files, create_test_misc_files, destination_root_directory,
                      source_directory, media_destination_year_directory, misc_destination_year_directory,
                      metadata_error_destination_year_directory, file_instance)
from test.fixtures.mock_capture_date_identifier import mock_capture_date_identifier_metadata_readable, \
    mock_capture_date_identifier_metadata_unreadable

from app.filepath_generator import FilepathGenerator
from app.mode_flags import ModeFlags, ModeFlagsMeta


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def run_with_media_flag_enabled(source_filepath, mock_capture_time_identifier):
    return FilepathGenerator(source_filepath, destination_root_directory,
                             mock_capture_time_identifier).generate_destination_filepath(media=True)


def run_with_media_flag_disabled(source_filepath, mock_capture_time_identifier):
    return FilepathGenerator(source_filepath, destination_root_directory,
                             mock_capture_time_identifier).generate_destination_filepath(media=False)


class TestSharedFunctionality:
    def test_generates_filepath(self, mock_capture_date_identifier_metadata_readable):
        _, source_filepath, destination_directory, expected_destination_path = create_test_media_files()
        generated_destination_path = run_with_media_flag_enabled(source_filepath,
                                                                 mock_capture_date_identifier_metadata_readable)

        assert generated_destination_path == expected_destination_path

    def test_increments_number_suffix_if_identical_destination_path_exists_in_db(
            self, mock_capture_date_identifier_metadata_readable):
        file_instance().save()
        _, source_filepath, destination_directory, _ = create_test_media_files()
        generated_destination_path = run_with_media_flag_enabled(source_filepath,
                                                                 mock_capture_date_identifier_metadata_readable)

        expected_destination_path = construct_path(destination_directory, 'test_media_file___1.jpeg')

        assert generated_destination_path == expected_destination_path

    def test_returns_none_if_identical_destination_path_and_size_exists_in_db(
            self, mock_capture_date_identifier_metadata_readable):
        file_instance(size=16).save()
        source_filepath = create_file_on_disk_with_data(source_directory, 'test_media_file.jpeg', 'this is 16 bytes')
        generated_destination_path = run_with_media_flag_enabled(source_filepath,
                                                                 mock_capture_date_identifier_metadata_readable)

        assert generated_destination_path is None

    def test_increments_number_suffix_if_existing_file_already_has_suffix_and_different_size(
            self, mock_capture_date_identifier_metadata_readable):
        _, source_filepath, destination_directory, _ = create_test_media_files(
            filename='a_file___1.jpeg', create_destination_file=True)

        generated_destination_path = run_with_media_flag_enabled(source_filepath,
                                                                 mock_capture_date_identifier_metadata_readable)
        expected_destination_path = construct_path(destination_directory, 'a_file___2.jpeg')

        assert generated_destination_path == expected_destination_path

    def test_returns_none_if_generated_path_points_to_identical_file(self,
                                                                     mock_capture_date_identifier_metadata_readable):
        data = 'same data'
        _, source_filepath, _, _ = create_test_media_files(
            filename='a_file___1.jpeg', source_data=data, dest_data=data, create_destination_file=True)
        generated_destination_path = run_with_media_flag_enabled(source_filepath,
                                                                 mock_capture_date_identifier_metadata_readable)

        assert generated_destination_path is None

    def test_returns_none_if_second_path_generated_points_to_file_with_identical_name_and_suffix_and_size(
            self, mock_capture_date_identifier_metadata_readable):
        filename = 'test_file.jpeg'
        source_filepath = create_file_on_disk_with_data(source_directory, filename, 'Same data')

        # source filepath has name clash with this filepath, so generated filename is incremented
        create_file_on_disk_with_data(media_destination_year_directory, filename, 'Unique data')
        # generated incremented filepath is identical, and files are same size/have same data
        create_file_on_disk_with_data(media_destination_year_directory, 'test_file___1.jpeg', 'Same data')

        generated_destination_path = FilepathGenerator(source_filepath,
                                                       destination_root_directory,
                                                       mock_capture_date_identifier_metadata_readable
                                                       ).generate_destination_filepath(media=True)

        assert generated_destination_path is None


class TestMediaFilesFunctionality:
    def test_adds_suffix_to_filename_if_existing_file_has_same_name_and_different_size_for_media_file(
            self, mock_capture_date_identifier_metadata_readable):
        filename, source_filepath, destination_directory, _ = create_test_media_files(
            create_destination_file=True)

        generated_destination_path = run_with_media_flag_enabled(source_filepath,
                                                                 mock_capture_date_identifier_metadata_readable)
        expected_filename = f'{Path(filename).stem}___1.jpeg'
        expected_destination_path = construct_path(destination_directory, expected_filename)

        assert generated_destination_path == expected_destination_path

    def test_generates_path_including_year_and_quarter(self, mock_capture_date_identifier_metadata_readable):
        filename, source_filepath, destination_directory, _ = create_test_media_files()

        generated_destination_path = run_with_media_flag_enabled(source_filepath,
                                                                 mock_capture_date_identifier_metadata_readable)
        expected_destination_path = construct_path(destination_directory, filename)

        assert generated_destination_path == expected_destination_path

    def test_files_are_sorted_into_folders_by_year_with_no_quarter_sub_folders_in_year_only_mode(
            self, mock_capture_date_identifier_metadata_readable):
        ModeFlagsMeta._instance = {}
        ModeFlags(year_mode=True)
        filename, source_filepath, _, _ = create_test_media_files()

        generated_destination_path = \
            FilepathGenerator(source_filepath, destination_root_directory,
                              mock_capture_date_identifier_metadata_readable).generate_destination_filepath(media=True)
        expected_destination_path = construct_path(destination_root_directory, '2023', filename)

        assert generated_destination_path == expected_destination_path

        ModeFlagsMeta._instance = {}
        ModeFlags(year_mode=False)


class TestMiscFilesFunctionality:
    def test_returns_none_if_generated_path_points_to_identical_file(self,
                                                                     mock_capture_date_identifier_metadata_readable):
        data = 'same data'
        _, source_filepath, _, _ = create_test_misc_files(
            filename='a_file___1.txt', source_data=data, dest_data=data, create_destination_file=True)
        generated_destination_path = run_with_media_flag_disabled(source_filepath,
                                                                  mock_capture_date_identifier_metadata_readable)

        assert generated_destination_path is None

    def test_returns_none_if_second_path_generated_points_to_file_with_identical_name_and_suffix_and_size(
            self, mock_capture_date_identifier_metadata_readable):
        filename = 'test_file.gif'
        source_filepath = create_file_on_disk_with_data(source_directory, filename, 'Same data')
        # source filepath has name clash with this filepath, so generated filename is incremented
        create_file_on_disk_with_data(misc_destination_year_directory, filename, 'Unique data')
        # generated incremented filepath is identical, and files are same size/have same data
        create_file_on_disk_with_data(misc_destination_year_directory, 'test_file___1.gif', 'Same data')

        generated_destination_path = FilepathGenerator(source_filepath,
                                                       destination_root_directory,
                                                       mock_capture_date_identifier_metadata_readable
                                                       ).generate_destination_filepath(media=False)

        assert generated_destination_path is None

    def test_adds_suffix_to_filename_if_existing_file_has_same_name_and_different_size_for_misc_file(
            self, mock_capture_date_identifier_metadata_readable):
        filename, source_filepath, destination_directory, _ = create_test_misc_files(
            create_destination_file=True)

        generated_destination_path = run_with_media_flag_disabled(source_filepath,
                                                                  mock_capture_date_identifier_metadata_readable)
        expected_filename = f'{Path(filename).stem}___1.gif'
        expected_destination_path = construct_path(destination_directory, expected_filename)

        assert generated_destination_path == expected_destination_path

    def test_misc_files_copied_to_year_based_destination_directories(self,
                                                                     mock_capture_date_identifier_metadata_readable):
        filename, source_filepath, destination_directory, _ = create_test_misc_files()

        generated_destination_path = run_with_media_flag_disabled(source_filepath,
                                                                  mock_capture_date_identifier_metadata_readable)
        expected_destination_path = construct_path(destination_directory, filename)

        assert generated_destination_path == expected_destination_path


class TestUnreadableMetadata:
    def test_copies_file_to_errors_folder_when_metadata_unreadable(self,
                                                                   mock_capture_date_identifier_metadata_unreadable):
        filename, source_filepath, destination_directory, _ = create_test_media_files()

        generated_destination_path = run_with_media_flag_enabled(source_filepath,
                                                                 mock_capture_date_identifier_metadata_unreadable)
        expected_destination_path = construct_path(metadata_error_destination_year_directory, filename)

        assert generated_destination_path == expected_destination_path
