from app.app_controller import AppController

from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_copies_file_to_generated_directory(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: "y")

    file_path = str(Path(__file__).parent) + '/media/target/2023/Q2/a_file___1.jpeg'

    assert not os.path.isfile(file_path)

    AppController().run(static_source_directory, target_root_directory)

    assert os.path.isfile(file_path)


def test_copies_file_when_paths_given_with_no_backslash_on_end(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: "y")

    file_path = str(Path(__file__).parent) + '/media/target/2023/Q2/a_file___1.jpeg'

    assert not os.path.isfile(file_path)

    source = static_source_directory[:-1]
    target = target_root_directory[:-1]

    AppController().run(source, target)

    assert os.path.isfile(file_path)


def test_throws_error_when_path_not_valid():
    with pytest.raises(FileNotFoundError):
        AppController().run(static_source_directory + 'jkjkjkjk', target_root_directory)