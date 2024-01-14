from datetime import datetime
from .helpers import (Path, clear_db_and_test_directories, construct_path, create_file_on_disk_with_data,
                      create_test_media_files, destination_root_directory, source_directory, static_destination_path)
from test.fixtures.filepath_generator_fixtures import *
from app.filepath_generator import FilepathGenerator


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_db_and_test_directories()


def run_with_media_flag_enabled(source_filepath):
    return FilepathGenerator(source_filepath, destination_root_directory
                             ).generate_destination_filepath(media=True)


def test_adds_suffix_to_filename_if_existing_file_has_same_name_and_different_size():
    filename, source_filepath, destination_directory, _ = create_test_media_files(
        create_destination_file=True)


class TestSharedFunctionality:
    def test_increments_number_suffix_if_existing_file_already_has_suffix_and_different_size(self):
        _, source_filepath, destination_directory, _ = create_test_media_files(
            filename='a_file___1.jpeg', create_destination_file=True)

        generated_destination_path = run_with_media_flag_enabled(source_filepath)
        expected_destination_path = construct_path(destination_directory, 'a_file___2.jpeg')

        assert generated_destination_path == expected_destination_path

    def test_returns_none_if_generated_path_points_to_identical_file(self):
        data = 'same data'
        _, source_filepath, _, _ = create_test_media_files(
            filename='a_file___1.jpeg', source_data=data, dest_data=data, create_destination_file=True)
        generated_destination_path = run_with_media_flag_enabled(source_filepath)

        assert generated_destination_path is None

    def test_returns_none_if_second_path_generated_points_to_file_with_identical_name_and_suffix_and_size(self):
        filename = 'test_file.jpeg'
        source_filepath = create_file_on_disk_with_data(source_directory, filename, 'Same data')
        destination_directory = static_destination_path(source_filepath)

        # source filepath has name clash with this filepath, so generated filename is incremented
        create_file_on_disk_with_data(destination_directory, filename, 'Unique data')
        # generated incremented filepath is identical, and files are same size/have same data
        create_file_on_disk_with_data(destination_directory, 'test_file___1.jpeg', 'Same data')

        generated_destination_path = FilepathGenerator(source_filepath,
                                                       destination_root_directory
                                                       ).generate_media_destination_filepath()

        assert generated_destination_path is None


class TestMediaFilesFunctionality:
    def test_adds_suffix_to_filename_if_existing_file_has_same_name_and_different_size_for_media_file(self):
        filename, source_filepath, destination_directory, _ = create_test_media_files(
            create_destination_file=True)

        generated_destination_path = run_with_media_flag_enabled(source_filepath)
        expected_filename = f'{Path(filename).stem}___1.jpeg'
        expected_destination_path = construct_path(destination_directory, expected_filename)

        assert generated_destination_path == expected_destination_path

    def test_generates_path_including_year_and_quarter(self):
        filename, source_filepath, destination_directory, _ = create_test_media_files()

        generated_destination_path = run_with_media_flag_enabled(source_filepath)
        expected_destination_path = construct_path(destination_directory, filename)

        assert generated_destination_path == expected_destination_path

    def test_uses_birth_time_for_capture_time_when_it_is_earliest_file_stat_time(self, birth_time_first):
        generated_date = FilepathGenerator('/source', '/destination')._approximate_media_capture_time()
        expected_date = datetime.fromtimestamp(birth_time_first.st_birthtime)

        assert expected_date == generated_date

    def test_uses_modified_time_for_capture_time_when_it_is_earliest_file_stat_time(self, modified_time_first):
        generated_date = FilepathGenerator('/source', '/destination')._approximate_media_capture_time()
        expected_date = datetime.fromtimestamp(modified_time_first.st_mtime)

        assert expected_date == generated_date

    def test_uses_creation_time_for_capture_time_when_it_is_earliest_file_stat_time(self, creation_time_first):
        generated_date = FilepathGenerator('/source', '/destination')._approximate_media_capture_time()
        expected_date = datetime.fromtimestamp(creation_time_first.st_ctime)

        assert expected_date == generated_date
