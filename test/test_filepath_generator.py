from app.filepath_generator import FilepathGenerator

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    clear_test_directories()


def test_generates_path_including_year_and_quarter():
    filename = 'test_file.jpeg'
    source_filepath = create_file(source_directory, filename)

    destination_directory = static_destination_path(source_filepath)

    generated_destination_path = FilepathGenerator(source_filepath, destination_root_directory
                                                   ).generate_destination_filepath()
    expected_destination_path = os.path.join(destination_directory, filename)

    assert expected_destination_path == generated_destination_path


def test_adds_suffix_to_filename_if_there_is_a_name_clash_with_existing_file():
    filename = 'file_1.jpeg'
    source_filepath = create_file(source_directory, filename)

    destination_directory = static_destination_path(source_filepath)

    create_file_with_data(destination_directory, filename, 'Some original data')

    path = FilepathGenerator(source_filepath, destination_root_directory).generate_destination_filepath()

    assert path == destination_directory + 'file_1___1.jpeg'


def test_increments_number_suffix_if_name_clashes_with_file_that_already_has_suffix():
    filename = 'a_file___1.jpeg'
    source_filepath = create_file(source_directory, filename)

    destination_directory = static_destination_path(source_filepath)

    create_file_with_data(destination_directory, filename, 'Some original data')

    path = FilepathGenerator(source_filepath, destination_root_directory).generate_destination_filepath()

    assert path == destination_directory + 'a_file___2.jpeg'


def test_returns_none_if_generated_path_points_to_identical_file():
    filename = 'this_file.jpeg'
    source_filepath = create_file_with_data(source_directory, filename, 'Same data')
    destination_directory = static_destination_path(source_filepath)

    create_file_with_data(destination_directory, filename, 'Same data')

    path = FilepathGenerator(source_filepath, destination_root_directory).generate_destination_filepath()

    assert path is None


def test_returns_none_if_second_path_generated_points_to_file_with_identical_name_suffix_and_size():
    filename = 'this_file.jpeg'
    source_filepath = create_file_with_data(source_directory, filename, 'Same data')
    destination_directory = static_destination_path(source_filepath)

    # source filepath has name clash with this filepath, so generated filename is incremented
    create_file_with_data(destination_directory, filename, 'Unique data')
    # generated incremented filepath is identical, and files are same size/have same data
    create_file_with_data(destination_directory, 'this_file___1.jpeg', 'Same data')

    path = FilepathGenerator(source_filepath, destination_root_directory).generate_destination_filepath()

    assert path is None
