from .helpers import clear_db_and_test_directories, instantiate_file_from_db_record
from test.fixtures.file_gateway_fixtures import *
from app.file import File
from app.file_gateway import FileGateway

gateway = FileGateway()


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_db_and_test_directories()


def test_can_read_and_write_file(file):
    gateway.insert(file)

    retrieved_file = instantiate_file_from_db_record(file.source_filepath)

    assert file == retrieved_file


def test_deletes_file(file, file_2):
    gateway.insert(file)
    gateway.insert(file_2)

    assert gateway.count() == 2

    gateway.delete(file.source_filepath)
    retrieved_file = instantiate_file_from_db_record(file_2.source_filepath)

    assert gateway.count() == 1
    assert file_2 == retrieved_file


def test_sums_size_of_all_files(file, file_2):
    gateway.insert(file)
    gateway.insert(file_2)

    assert gateway.sum_size() == 16


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


def test_updates_copied_and_copy_attempted_fields_to_denote_copy_success(file):
    gateway.insert(file)
    file.copied = True
    file.copy_attempted = True
    gateway.update_copied(file.copied, file.copy_attempted, file.source_filepath)

    file = instantiate_file_from_db_record(file.source_filepath)

    assert file.copied is True
    assert file.copy_attempted is True


def test_updates_copied_and_copy_attempted_fields_to_denote_copy_failure(file):
    gateway.insert(file)
    file.copied = False
    file.copy_attempted = True
    gateway.update_copied(file.copied, file.copy_attempted, file.source_filepath)

    file = instantiate_file_from_db_record(file.source_filepath)

    assert file.copied is False
    assert file.copy_attempted is True


def test_counts_duplicate_files(duplicate_file):
    gateway.insert(duplicate_file)

    assert gateway.duplicate_count() == 1


def test_counts_name_clashes(file_with_name_clash):
    gateway.insert(file_with_name_clash)

    assert gateway.name_clash_count() == 1


def test_selects_file_where_copy_not_attempted(
        copied_file, file_with_copy_error, uncopied_file, duplicate_file):
    for f in [copied_file, file_with_copy_error, uncopied_file, duplicate_file]:
        gateway.insert(f)

    record = gateway.select_one_where_copy_not_attempted()
    selected_file = File.init_from_record(record)

    assert selected_file == uncopied_file

    # confirm that it was just one record that met the criteria
    gateway.delete(uncopied_file.source_filepath)
    selected_record = gateway.select_one_where_copy_not_attempted()

    assert selected_record is None


def test_when_attempting_to_select_uncopied_file_it_returns_none_when_no_valid_records_exist(
        copied_file, file_with_copy_error):
    gateway.insert(copied_file)
    gateway.insert(file_with_copy_error)

    record = gateway.select_one_where_copy_not_attempted()

    assert record is None


def test_sums_size_of_files_that_are_valid_candidates_for_copying(
        uncopied_file, uncopied_file_2, not_to_copy):
    for f in [uncopied_file, uncopied_file_2, not_to_copy]:
        gateway.insert(f)

    sum_of_file_sizes = gateway.sum_size_of_files_to_be_copied()
    size_of_files_to_be_copied = uncopied_file.size + uncopied_file_2.size

    assert sum_of_file_sizes == size_of_files_to_be_copied
