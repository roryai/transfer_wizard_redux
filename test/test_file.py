from .helpers import *

gateway = FileGateway()


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_database()


def test_inserted_and_retrieved_files_are_identical():
    file = file_instance()
    file.save()

    record = gateway.select_all()[0]
    retrieved_file = File.init_from_record(record)

    assert file == retrieved_file


def test_determines_file_directory():
    assert str(file_instance().destination_directory()) == '/destination'
