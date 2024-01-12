from test.fixtures.file_gateway_fixtures import *

gateway = FileGateway()


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_database()
    clear_test_directories()


def test_can_read_and_write_file(file):
    gateway.insert(file)

    retrieved_file = instantiate_file_from_db_record()

    assert file == retrieved_file


def test_sums_size_of_all_files(file, file_2):
    gateway.insert(file)
    gateway.insert(file_2)

    assert gateway.sum_size() == 2048


def test_counts_file_rows(file, file_2):
    gateway.insert(file)
    gateway.insert(file_2)

    assert gateway.count() == 2


def test_deletes_rows(file):
    assert gateway.count() == 0

    gateway.insert(file)

    assert gateway.count() == 1

    gateway.wipe_database()

    assert gateway.count() == 0


def test_source_filepath_must_be_unique(
        same_source_different_destination_1, same_source_different_destination_2):
    gateway.insert(same_source_different_destination_1)
    gateway.insert(same_source_different_destination_2)

    assert gateway.count() == 1


def test_destination_filepath_must_be_unique(
        different_source_same_destination_1, different_source_same_destination_2):
    gateway.insert(different_source_same_destination_1)
    gateway.insert(different_source_same_destination_2)

    assert gateway.count() == 1


def test_updates_copied_field_to_true(file):
    gateway.insert(file)

    file = instantiate_file_from_db_record()

    assert file.copied is None

    file.copied = True
    gateway.update_copied(file)

    file = instantiate_file_from_db_record()

    assert file.copied is True


def test_updates_copied_field_to_false(file):
    gateway.insert(file)

    file = instantiate_file_from_db_record()

    assert file.copied is None

    file.copied = False
    gateway.update_copied(file)

    file = instantiate_file_from_db_record()

    assert file.copied is False


def test_default_copied_value_is_null(file):  # TODO delete this when updating copied field to non null
    gateway.insert(file)

    record = gateway.select_all()[0]

    assert record[4] is None


def test_counts_duplicate_files(duplicate_file):
    gateway.insert(duplicate_file)

    assert gateway.duplicate_count() == 1


def test_counts_name_clashes(file_with_name_clash):
    gateway.insert(file_with_name_clash)

    assert gateway.name_clash_count() == 1


def test_selects_uncopied_file_with_no_name_clash_for_copying(
        copied_file, file_with_copy_error, file, duplicate_file):
    for f in [copied_file, file_with_copy_error, file, duplicate_file]:
        gateway.insert(f)

    copied_file.copied = True
    file_with_copy_error.copied = False
    for f in [copied_file, file_with_copy_error]:
        gateway.update_copied(f)

    selected_file = File.init_from_record(gateway.select_one_file_where_copy_not_attempted())

    assert selected_file == file

    file.copied = True
    gateway.update_copied(file)
    selected_record = gateway.select_one_file_where_copy_not_attempted()

    # confirm that it was just one record that met the criteria
    assert selected_record is None


def test_selects_uncopied_file_with_name_clash_for_copying(
        copied_file, file_with_copy_error, file_with_name_clash, duplicate_file):
    for f in [copied_file, file_with_copy_error, file_with_name_clash, duplicate_file]:
        gateway.insert(f)

    copied_file.copied = True
    file_with_copy_error.copied = False
    for f in [copied_file, file_with_copy_error]:
        gateway.update_copied(f)

    selected_file = File.init_from_record(gateway.select_one_file_where_copy_not_attempted())

    assert selected_file == file_with_name_clash

    file_with_name_clash.copied = True
    gateway.update_copied(file_with_name_clash)
    selected_record = gateway.select_one_file_where_copy_not_attempted()

    # confirm that it was just one record that met the criteria
    assert selected_record is None


def test_when_attempting_to_select_uncopied_file_it_returns_none_when_no_valid_records_exist(
        copied_file, file_with_copy_error):
    gateway.insert(copied_file)
    gateway.insert(file_with_copy_error)
    copied_file.copied = True
    file_with_copy_error.copied = False
    for f in [copied_file, file_with_copy_error]:
        gateway.update_copied(f)

    record = gateway.select_one_file_where_copy_not_attempted()

    assert record is None


def test_sums_size_of_files_that_are_valid_candidates_for_copying(
        to_be_copied_1, to_be_copied_2, not_to_copy):
    for f in [to_be_copied_1, to_be_copied_2, not_to_copy]:
        gateway.insert(f)

    sum_of_file_sizes = gateway.sum_size_of_files_to_be_copied()
    size_of_files_to_be_copied = to_be_copied_1.size + to_be_copied_2.size

    assert sum_of_file_sizes == size_of_files_to_be_copied
