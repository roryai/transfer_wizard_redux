from app.file import File
from .helpers import *

gateway = FileGateway()
file = File(source_filepath='/source',
            destination_filepath='/destination',
            size=1024,
            name_clash=False)


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_database()


def test_can_insert_and_read_record():
    gateway.insert(file)

    record = gateway.select_all()[0]

    assert file.source_filepath == record[1]
    assert file.destination_filepath == record[2]
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


def test_selects_no_copy_attempted_file_that_has_destination_path_and_no_name_clash_for_copying():
    simple_file = File(source_filepath='/source/valid_candidate_file',
                       destination_filepath='/destination',
                       size=1024,
                       name_clash=False)
    copied_file = File(source_filepath='/source/copied_file',
                       destination_filepath='/destination',
                       size=1024,
                       name_clash=False)
    file_with_copy_error = File(source_filepath='/source/file_with_copy_error',
                                destination_filepath='/destination',
                                size=1024,
                                name_clash=False)
    duplicate_file = File(source_filepath='/source/duplicate_file',
                          destination_filepath='',
                          size=1024,
                          name_clash=False)

    for f in [copied_file, file_with_copy_error, simple_file, duplicate_file]:
        gateway.insert(f)

    copied_file.copied = True
    file_with_copy_error.copied = False
    for f in [copied_file, file_with_copy_error]:
        gateway.update_copied(f)

    selected_file = File.init_from_record(gateway.select_one_file_where_copy_not_attempted())

    assert selected_file == simple_file

    # confirm that it was just one record that met the criteria
    simple_file.copied = True
    gateway.update_copied(simple_file)
    selected_record = gateway.select_one_file_where_copy_not_attempted()

    assert selected_record is None


def test_selects_no_copy_attempted_file_that_has_destination_path_and_has_name_clash_for_copying():
    file_with_name_clash = File(source_filepath='/source/valid_name_clash_file',
                                destination_filepath='/destination',
                                size=1024,
                                name_clash=True)
    copied_file = File(source_filepath='/source/copied_file',
                       destination_filepath='/destination',
                       size=1024,
                       name_clash=False)
    file_with_copy_error = File(source_filepath='/source/file_with_copy_error',
                                destination_filepath='/destination',
                                size=1024,
                                name_clash=False)
    duplicate_file = File(source_filepath='/source/duplicate_file',
                          destination_filepath='',
                          size=1024,
                          name_clash=False)

    for f in [copied_file, file_with_copy_error, file_with_name_clash, duplicate_file]:
        gateway.insert(f)

    copied_file.copied = True
    file_with_copy_error.copied = False
    for f in [copied_file, file_with_copy_error]:
        gateway.update_copied(f)

    selected_file = File.init_from_record(gateway.select_one_file_where_copy_not_attempted())

    assert selected_file == file_with_name_clash

    # confirm that it was just one record that met the criteria
    file_with_name_clash.copied = True
    gateway.update_copied(file_with_name_clash)
    selected_record = gateway.select_one_file_where_copy_not_attempted()

    assert selected_record is None


def test_when_selecting_copy_not_attempted_file_it_returns_none_when_no_valid_records_exist():
    copied_file = File(source_filepath='/source',
                       destination_filepath='/destination',
                       size=1024,
                       name_clash=False)
    file_with_copy_error = File(source_filepath='/source/file_with_copy_error',
                                destination_filepath='/destination',
                                size=1024,
                                name_clash=False)

    gateway.insert(copied_file)
    gateway.insert(file_with_copy_error)
    copied_file.copied = True
    file_with_copy_error.copied = False
    for f in [copied_file, file_with_copy_error]:
        gateway.update_copied(f)

    record = gateway.select_one_file_where_copy_not_attempted()

    assert record is None


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


def test_sums_size_of_files_that_are_valid_candidates_for_copying():
    to_be_copied_1 = File(source_filepath='/source',
                          destination_filepath='/destination',
                          size=1024,
                          name_clash=False)
    to_be_copied_2 = File(source_filepath='/source/file_without_copy_error',
                          destination_filepath='/destination',
                          size=2048,
                          name_clash=True)
    not_to_copy = File(source_filepath='/source/',
                       destination_filepath='',
                       size=10,
                       name_clash=False)

    for f in [to_be_copied_1, to_be_copied_2, not_to_copy]:
        gateway.insert(f)

    sum = gateway.sum_size_of_files_to_be_copied()
    size_of_files_to_be_copied = to_be_copied_1.size + to_be_copied_2.size

    assert sum == size_of_files_to_be_copied
