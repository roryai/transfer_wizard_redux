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

    AppController(static_source_directory, target_root_directory).run()

    assert os.path.isfile(file_path)
