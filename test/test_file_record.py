from .helpers import *

from app.file_record import FileRecord


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_database()


def test_inserts_and_maps_a_file():
    file_instance().save()

    gateway = FileGateway()
    assert gateway.count() == 1
    result = FileRecord().map_from_record(gateway.select_all()[0])

    assert result['source_filepath'] == default_source_filepath
    assert result['destination_filepath'] == default_destination_filepath
    assert result['size'] == 1024
    assert result['name_clash'] is 0
    assert result['copied'] is 0
    assert result['media'] is 1
    assert result['copy_attempted'] is 0
    assert len(result) == 7
