from main import main

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_copies_desired_file_to_generated_directory():
    file_path = str(Path(__file__).parent) + '/media/target/2023/Q2/a_file___1.jpeg'

    assert not os.path.isfile(file_path)

    main(static_source_directory, target_root_directory)

    assert os.path.isfile(file_path)


def test_copies_file_when_paths_given_with_no_backslash_on_end():
    file_path = str(Path(__file__).parent) + '/media/target/2023/Q2/a_file___1.jpeg'

    assert not os.path.isfile(file_path)

    source = static_source_directory[:-1]
    target = target_root_directory[:-1]

    main(source, target)

    assert os.path.isfile(file_path)


def test_throws_error_when_path_not_valid():
    with pytest.raises(FileNotFoundError):
        main(static_source_directory + 'jkjkjkjk', target_root_directory)
