from .helpers import cleanup, instantiate_file_from_db_record
from test.fixtures.shared_fixtures import *
from app.file import File
from app.file_gateway import FileGateway

gateway = FileGateway()


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def insert_records(*args):
    for record in [*args]:
        gateway.insert(record)


def test_can_read_and_write_file(file):
    gateway.insert(file)
    print("")
    retrieved_file = instantiate_file_from_db_record(file.source_filepath)

    assert file == retrieved_file


def test_selects_file_where_copy_not_attempted(
        copied_media_file, file_with_copy_error, uncopied_media_file, duplicate_media_file):
    insert_records(copied_media_file, file_with_copy_error, uncopied_media_file, duplicate_media_file)

    record = gateway.select_one_where_copy_not_attempted()
    selected_file = File.init_from_record(record)

    assert selected_file == uncopied_media_file

    # confirm that it was just one record that met the criteria
    gateway.delete(uncopied_media_file.source_filepath)
    selected_record = gateway.select_one_where_copy_not_attempted()

    assert selected_record is None


def test_when_attempting_to_select_uncopied_file_it_returns_none_when_no_valid_records_exist(
        copied_media_file, file_with_copy_error):
    insert_records(copied_media_file, file_with_copy_error)

    record = gateway.select_one_where_copy_not_attempted()

    assert record is None


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


def test_deletes_file(file, file_2):
    insert_records(file, file_2)

    assert gateway.count() == 2

    gateway.delete(file.source_filepath)
    retrieved_file = instantiate_file_from_db_record(file_2.source_filepath)

    assert gateway.count() == 1
    assert file_2 == retrieved_file


def test_wipes_database(file, file_2):
    insert_records(file, file_2)

    assert gateway.count() == 2

    gateway.wipe_database()

    assert gateway.count() == 0


def test_counts_records(file, file_2):
    insert_records(file, file_2)

    assert gateway.count() == 2


def test_counts_files_to_be_copied(file, duplicate_media_file):
    insert_records(file, duplicate_media_file)

    assert gateway.count_files_to_be_copied() == 1


def test_counts_duplicate_files(duplicate_media_file):
    gateway.insert(duplicate_media_file)

    assert gateway.duplicate_count() == 1


def test_counts_name_clashes(media_file_with_name_clash):
    gateway.insert(media_file_with_name_clash)

    assert gateway.name_clash_count() == 1


def test_detects_whether_destination_filepath_is_in_use(uncopied_media_file):
    assert gateway.destination_filepath_in_use(uncopied_media_file.destination_filepath) is False

    gateway.insert(uncopied_media_file)

    assert gateway.destination_filepath_in_use(uncopied_media_file.destination_filepath) is True


def test_selects_identical_destination_path_and_size_record(uncopied_media_file):
    gateway.insert(uncopied_media_file)

    record = gateway.select_duplicate_file(uncopied_media_file.destination_filepath, uncopied_media_file.size)
    file = File.init_from_record(record)
    assert file == uncopied_media_file


def test_detects_whether_record_with_same_size_and_destination_filepath_exists(uncopied_media_file):
    assert gateway.identical_size_and_destination_filepath_record_exists(
        uncopied_media_file.destination_filepath, uncopied_media_file.size) is False

    gateway.insert(uncopied_media_file)

    assert gateway.identical_size_and_destination_filepath_record_exists(
        uncopied_media_file.destination_filepath, uncopied_media_file.size) is True


def test_sums_size_of_all_files(file, file_2):
    insert_records(file, file_2)

    assert gateway.sum_size() == file.size + file_2.size


def test_sums_size_of_name_clash_files(
        media_file_with_name_clash, misc_file_with_name_clash, copied_misc_file):
    insert_records(media_file_with_name_clash, misc_file_with_name_clash, copied_misc_file)

    sum_of_file_sizes = gateway.sum_size_of_name_clash_files()
    size_of_files_to_be_copied = \
        media_file_with_name_clash.size + misc_file_with_name_clash.size

    assert sum_of_file_sizes == size_of_files_to_be_copied


def test_sums_size_of_duplicate_files(
        duplicate_media_file, duplicate_misc_file, copied_misc_file):
    insert_records(duplicate_media_file, duplicate_misc_file, copied_misc_file)

    sum_of_file_sizes = gateway.sum_size_of_duplicate_files()
    size_of_files_to_be_copied = \
        duplicate_media_file.size + duplicate_misc_file.size

    assert sum_of_file_sizes == size_of_files_to_be_copied


def test_sums_size_of_files_that_are_valid_candidates_for_copying(
        uncopied_media_file, uncopied_media_file_2, duplicate_media_file):
    insert_records(uncopied_media_file, uncopied_media_file_2, duplicate_media_file)

    sum_of_file_sizes = gateway.sum_size_of_files_to_be_copied()
    size_of_files_to_be_copied = uncopied_media_file.size + uncopied_media_file_2.size

    assert sum_of_file_sizes == size_of_files_to_be_copied


def test_source_filepath_must_be_unique(
        same_source_different_destination_1, same_source_different_destination_2):
    insert_records(same_source_different_destination_1, same_source_different_destination_2)

    assert gateway.count() == 1


def test_destination_filepath_must_be_unique(
        different_source_same_destination_1, different_source_same_destination_2):
    insert_records(different_source_same_destination_1, different_source_same_destination_2)

    assert gateway.count() == 1
