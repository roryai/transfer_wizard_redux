from app.db_initializer import DBInitializer
from app.file import File
from .helpers import *


DBInitializer().init_test_database()


def test_can_insert_and_read_record():
    file = File('/source', '/target', 1024)
    file.insert_into_db()

    record = FileGateway().select_all()[0]
    retrieved_file = File.init_from_record(record)

    assert file == retrieved_file
