from .helpers import *

gateway = FileGateway()


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_database()


def test_inserted_and_retrieved_files_are_identical():
    file = file_instance()
    file.save()

    retrieved_file = instantiate_file_from_db_record()

    assert file == retrieved_file


def test_determines_file_directory():
    assert str(file_instance().destination_directory()) == '/destination'
