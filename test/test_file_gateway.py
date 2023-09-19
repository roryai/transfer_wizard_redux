from app.file import File
from .helpers import *

gateway = FileGateway()
file = File(source_filepath='/source',
            target_filepath='/target',
            size=1024,
            name_clash=False)


@pytest.fixture(autouse=True)
def teardown():
    clear_database()


def test_can_insert_and_read_record():
    gateway.insert(file)

    record = gateway.select_all()[0]

    assert file.source_filepath == record[1]
    assert file.target_filepath == record[2]
    assert file.size == record[3]
    assert file.copied == record[4]
    assert file.name_clash == record[5]


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


def test_selects_a_file_where_copy_has_not_been_attempted():
    copied_file = File(source_filepath='/source',
                       target_filepath='/target',
                       size=1024,
                       copied=True,
                       name_clash=False)

    file_with_copy_error = File(source_filepath='/source',
                                target_filepath='/target',
                                size=1024,
                                copied=False,
                                name_clash=False)

    no_copy_attempted_file = File(source_filepath='/source',
                                  target_filepath='/target',
                                  size=1024,
                                  copied=None,
                                  name_clash=False)

    for f in [copied_file, file_with_copy_error, no_copy_attempted_file]:
        gateway.insert(f)

    selected_file = File.init_from_record(gateway.select_one_file_where_copy_not_attempted())

    assert selected_file == no_copy_attempted_file


def test_updates_copied_field_to_true():
    gateway.insert(file)
    file.copied = True
    gateway.update_copied(file)

    record = gateway.select_all()[0]

    assert record[4] is 1


def test_updates_copied_field_to_false():
    gateway.insert(file)
    file.copied = False
    gateway.update_copied(file)

    record = gateway.select_all()[0]

    assert record[4] is 0


def test_default_copied_value_is_null():
    gateway.insert(file)

    record = gateway.select_all()[0]

    assert record[4] is None
