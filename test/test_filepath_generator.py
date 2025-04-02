from datetime import datetime

from .helpers import (pytest, Path, cleanup, construct_path, create_file_on_disk_with_data,
                      create_test_media_files, create_test_misc_files, destination_root_directory,
                      source_directory, media_destination_year_directory, misc_destination_year_directory,
                      file_instance)

from app.filepath_generator import FilepathGenerator
from app.mode_flags import ModeFlags, ModeFlagsMeta


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


@pytest.fixture(autouse=True)
def mock_capture_date_identifier(mocker):
    mock_class = mocker.patch("app.filepath_generator.CaptureDateIdentifier")
    mock_class.return_value.media_capture_date.return_value = datetime(2023, 12, 3)


def generate_filepath(source_filepath):
    return FilepathGenerator(source_filepath, destination_root_directory
                             ).generate_destination_filepath(media=True)


def generate_misc_filepath(source_filepath):
    return FilepathGenerator(source_filepath, destination_root_directory
                             ).generate_destination_filepath(media=False)


class TestSharedFunctionality:
    def test_generates_filepath(self):
        _, source_filepath, destination_directory, expected_destination_path = create_test_media_files()
        generated_destination_path = generate_filepath(source_filepath)

        assert generated_destination_path == expected_destination_path

    def test_increments_number_suffix_if_identical_destination_path_exists_in_db(
            self):
        file_instance().save()
        _, source_filepath, destination_directory, _ = create_test_media_files()
        generated_destination_path = generate_filepath(source_filepath)

        expected_destination_path = construct_path(destination_directory, 'test_media_file___1.jpeg')

        assert generated_destination_path == expected_destination_path

    def test_returns_none_if_identical_destination_path_and_size_exists_in_db(
            self):
        file_instance(size=16).save()
        source_filepath = create_file_on_disk_with_data(source_directory, 'test_media_file.jpeg', 'this is 16 bytes')
        generated_destination_path = generate_filepath(source_filepath)

        assert generated_destination_path is None

    def test_increments_number_suffix_if_existing_file_already_has_suffix_and_different_size(
            self):
        _, source_filepath, destination_directory, _ = create_test_media_files(
            filename='a_file___1.jpeg', create_destination_file=True)

        generated_destination_path = generate_filepath(source_filepath)
        expected_destination_path = construct_path(destination_directory, 'a_file___2.jpeg')

        assert generated_destination_path == expected_destination_path

    def test_returns_none_if_generated_path_points_to_identical_file(self):
        data = 'same data'
        _, source_filepath, _, _ = create_test_media_files(
            filename='a_file___1.jpeg', source_data=data, dest_data=data, create_destination_file=True)
        generated_destination_path = generate_filepath(source_filepath)

        assert generated_destination_path is None

    def test_returns_none_if_second_path_generated_points_to_file_with_identical_name_and_suffix_and_size(
            self):
        filename = 'test_file.jpeg'
        source_filepath = create_file_on_disk_with_data(source_directory, filename, 'Same data')

        # source filepath has name clash with this filepath, so generated filename is incremented
        create_file_on_disk_with_data(media_destination_year_directory, filename, 'Unique data')
        # generated incremented filepath is identical, and files are same size/have same data
        create_file_on_disk_with_data(media_destination_year_directory, 'test_file___1.jpeg', 'Same data')

        generated_destination_path = FilepathGenerator(source_filepath,
                                                       destination_root_directory
                                                       ).generate_destination_filepath(media=True)

        assert generated_destination_path is None


class TestMediaFilesFunctionality:
    def test_adds_suffix_to_filename_if_existing_file_has_same_name_and_different_size_for_media_file(
            self):
        filename, source_filepath, destination_directory, _ = create_test_media_files(
            create_destination_file=True)

        generated_destination_path = generate_filepath(source_filepath)
        expected_filename = f'{Path(filename).stem}___1.jpeg'
        expected_destination_path = construct_path(destination_directory, expected_filename)

        assert generated_destination_path == expected_destination_path

    def test_generates_path_including_year_and_quarter(self):
        filename, source_filepath, destination_directory, _ = create_test_media_files()

        generated_destination_path = generate_filepath(source_filepath)
        expected_destination_path = construct_path(destination_directory, filename)

        assert generated_destination_path == expected_destination_path

    def test_files_are_sorted_into_folders_by_year_with_no_quarter_sub_folders_in_year_only_mode(
            self):
        ModeFlagsMeta._instance = {}
        ModeFlags(year_mode=True)
        filename, source_filepath, _, _ = create_test_media_files()

        generated_destination_path = \
            FilepathGenerator(source_filepath, destination_root_directory).generate_destination_filepath(media=True)
        expected_destination_path = construct_path(destination_root_directory, '2023', filename)

        assert generated_destination_path == expected_destination_path

        ModeFlagsMeta._instance = {}
        ModeFlags(year_mode=False)


class TestMiscFilesFunctionality:
    def test_returns_none_if_generated_path_points_to_identical_file(self):
        data = 'same data'
        _, source_filepath, _, _ = create_test_misc_files(
            filename='a_file___1.txt', source_data=data, dest_data=data, create_destination_file=True)
        generated_destination_path = generate_misc_filepath(source_filepath)

        assert generated_destination_path is None

    def test_returns_none_if_second_path_generated_points_to_file_with_identical_name_and_suffix_and_size(
            self):
        filename = 'test_file.gif'
        source_filepath = create_file_on_disk_with_data(source_directory, filename, 'Same data')
        # source filepath has name clash with this filepath, so generated filename is incremented
        create_file_on_disk_with_data(misc_destination_year_directory, filename, 'Unique data')
        # generated incremented filepath is identical, and files are same size/have same data
        create_file_on_disk_with_data(misc_destination_year_directory, 'test_file___1.gif', 'Same data')

        generated_destination_path = FilepathGenerator(source_filepath,
                                                       destination_root_directory,
                                                       ).generate_destination_filepath(media=False)

        assert generated_destination_path is None

    def test_adds_suffix_to_filename_if_existing_file_has_same_name_and_different_size_for_misc_file(
            self):
        filename, source_filepath, destination_directory, _ = create_test_misc_files(
            create_destination_file=True)

        generated_destination_path = generate_misc_filepath(source_filepath)
        expected_filename = f'{Path(filename).stem}___1.gif'
        expected_destination_path = construct_path(destination_directory, expected_filename)

        assert generated_destination_path == expected_destination_path

    def test_misc_files_copied_to_year_based_destination_directories(self):
        filename, source_filepath, destination_directory, _ = create_test_misc_files()

        generated_destination_path = generate_misc_filepath(source_filepath)
        expected_destination_path = construct_path(destination_directory, filename)

        assert generated_destination_path == expected_destination_path
