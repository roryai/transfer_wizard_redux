from .helpers import pytest, cleanup, default_destination_media_filepath, default_source_media_filepath, file_instance
from app.file_gateway import FileGateway
from app.file_record import FileRecord


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def test_inserts_and_maps_a_file():
    file = file_instance()
    file.save()

    gateway = FileGateway()
    assert gateway.count() == 1
    result = FileRecord().map_from_record(gateway.select(file.source_filepath))

    assert result['source_filepath'] == default_source_media_filepath
    assert result['destination_filepath'] == default_destination_media_filepath
    assert result['size'] == 1024
    assert result['name_clash'] is False
    assert result['copied'] is False
    assert result['copy_attempted'] is False
    assert len(result) == 6
