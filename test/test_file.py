from app.file import File
from .helpers import *

gateway = FileGateway()


@pytest.fixture(autouse=True)
def teardown():
    clear_database()


def test_can_insert_and_read_record():
    file = File(source_filepath='/source',
                target_filepath='/target',
                size=1024,
                name_clash=False)
    file.save()

    record = gateway.select_all()[0]
    retrieved_file = File.init_from_record(record)

    assert file == retrieved_file


def test_sets_name_clash_attribute_when_value_is_true():
    file = File(source_filepath='/source',
                target_filepath='/target',
                size=1024,
                name_clash=True)
    file.save()

    record = gateway.select_all()[0]
    retrieved_file = File.init_from_record(record)

    assert retrieved_file.name_clash is True


def test_sets_name_clash_attribute_when_value_is_false():
    file = File(source_filepath='/source',
                target_filepath='/target',
                size=1024,
                name_clash=False)
    file.save()

    record = gateway.select_all()[0]
    retrieved_file = File.init_from_record(record)

    assert retrieved_file.name_clash is False


def test_sets_copied_attribute_to_none_by_default():
    file = File(source_filepath='/source',
                target_filepath='/target',
                size=1024,
                name_clash=False)
    file.save()

    record = gateway.select_all()[0]
    retrieved_file = File.init_from_record(record)

    assert retrieved_file.copied is None


def test_sets_copied_attribute_when_value_is_true():
    file = File(source_filepath='/source',
                target_filepath='/target',
                size=1024,
                name_clash=False)
    file.save()
    file.copied = True
    gateway.update_copied(file)

    record = gateway.select_all()[0]
    retrieved_file = File.init_from_record(record)

    assert retrieved_file.copied is True


def test_sets_copied_attribute_when_value_is_false():
    file = File(source_filepath='/source',
                target_filepath='/target',
                size=1024,
                name_clash=False)
    file.save()
    file.copied = False
    gateway.update_copied(file)

    record = gateway.select_all()[0]
    retrieved_file = File.init_from_record(record)

    assert retrieved_file.copied is False
