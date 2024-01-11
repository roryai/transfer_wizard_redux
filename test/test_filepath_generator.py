from app.filepath_generator import FilepathGenerator

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def setup_and_run_test_class(filename='test_file.jpeg', run_func=True,
                             source_data='default_source_data', dest_data='default_dest_data'):
    func = create_file_with_data
    source_filepath = func(source_directory, filename, source_data)
    destination_directory = static_destination_path(source_filepath)
    func(destination_directory, filename, dest_data) if run_func else None
    generated_destination_path = FilepathGenerator(source_filepath, destination_root_directory
                                                   ).generate_destination_filepath()
    return filename, source_filepath, destination_directory, generated_destination_path


def test_generates_path_including_year_and_quarter():
    filename, _, destination_directory, generated_destination_path = setup_and_run_test_class(
        run_func=False)

    expected_destination_path = os.path.join(destination_directory, filename)

    assert generated_destination_path == expected_destination_path


def test_adds_suffix_to_filename_if_there_is_a_name_clash_with_existing_file():
    filename, _, destination_directory, generated_destination_path = setup_and_run_test_class()

    expected_destination_path = os.path.join(destination_directory, Path(filename).stem + '___1.jpeg')

    assert generated_destination_path == expected_destination_path


def test_increments_number_suffix_if_name_clashes_with_file_that_already_has_suffix():
    _, _, destination_directory, generated_destination_path = setup_and_run_test_class(
        filename='a_file___1.jpeg')

    expected_destination_path = os.path.join(destination_directory, 'a_file___2.jpeg')

    assert generated_destination_path == expected_destination_path


def test_returns_none_if_generated_path_points_to_identical_file():
    data = 'same data'
    _, _, _, generated_destination_path = setup_and_run_test_class(
        filename='a_file___1.jpeg', source_data=data, dest_data=data)

    assert generated_destination_path is None


def test_returns_none_if_second_path_generated_points_to_file_with_identical_name_and_suffix_and_size():
    filename = 'test_file.jpeg'
    source_filepath = create_file_with_data(source_directory, filename, 'Same data')
    destination_directory = static_destination_path(source_filepath)

    # source filepath has name clash with this filepath, so generated filename is incremented
    create_file_with_data(destination_directory, filename, 'Unique data')
    # generated incremented filepath is identical, and files are same size/have same data
    create_file_with_data(destination_directory, 'test_file___1.jpeg', 'Same data')

    generated_destination_path = FilepathGenerator(source_filepath,
                                                   destination_root_directory).generate_destination_filepath()

    assert generated_destination_path is None
