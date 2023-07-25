import pytest

from main import main
from .test_helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def test_main():
    file_path = str(Path(__file__).parent) + '/media/target/2023/Q2/a_file___1.jpeg'

    assert not os.path.isfile(file_path)

    main()

    assert os.path.isfile(file_path)
