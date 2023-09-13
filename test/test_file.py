from app.file import File
from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_database()


def test_can_insert_and_read_record():
    file = File('/source', '/target', 1024, False)
    file.save()

    record = FileGateway().select_all()[0]
    retrieved_file = File.init_from_record(record)

    assert file == retrieved_file
