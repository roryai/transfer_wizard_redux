from app.file import File
from .helpers import *


gateway = FileGateway()
file = File('/source', '/target', 1024, False)


@pytest.fixture(autouse=True)
def teardown():
    clear_database()


def test_can_insert_and_read_record():
    gateway.insert(file)

    record = gateway.select_all()[0]

    assert file.source_filepath == record[1]
    assert file.target_filepath == record[2]
    assert file.size == record[3]
    assert file.name_clash == record[4]


def test_sums_size_of_all_files():
    gateway.insert(file)
    gateway.insert(file)

    assert gateway.sum_size() == 2048


def test_counts_file_rows():
    gateway.insert(file)
    gateway.insert(file)
    gateway.insert(file)

    assert gateway.count() == 3


def test_deletes_rows():
    assert gateway.count() == 0

    gateway.insert(file)

    assert gateway.count() == 1

    gateway.wipe_database()

    assert gateway.count() == 0
