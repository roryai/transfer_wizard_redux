from .helpers import (pytest, cleanup, construct_path, destination_root_directory,
                      image_with_metadata_source_filepath, instantiate_file_from_db_record,
                      prepare_test_media_destination_name_clash_file, image_with_metadata_destination_directory,
                      prepare_test_media_source_file, prepare_test_media_destination_duplicate_file,
                      image_with_metadata_filesize)
from app.file_factory import FileFactory


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def save_pre_copy_file_record(source_filepath):
    FileFactory(source_filepath, destination_root_directory).save_pre_copy_file_record()


def test_a_media_file_is_built_and_saved():
    destination_filepath = prepare_test_media_source_file()

    save_pre_copy_file_record(image_with_metadata_source_filepath)

    file = instantiate_file_from_db_record(image_with_metadata_source_filepath)

    assert file.source_filepath == image_with_metadata_source_filepath
    assert file.destination_filepath == destination_filepath
    assert file.size == image_with_metadata_filesize
    assert file.name_clash is False
    assert file.copied is False


def test_file_is_marked_as_having_name_clash_when_an_existing_destination_file_has_same_name_and_different_size():
    prepare_test_media_source_file()
    prepare_test_media_destination_name_clash_file()

    save_pre_copy_file_record(image_with_metadata_source_filepath)

    file = instantiate_file_from_db_record(image_with_metadata_source_filepath)
    expected_filename = 'RRY01936___1.JPG'

    assert file.source_filepath == image_with_metadata_source_filepath
    assert file.destination_filepath == construct_path(image_with_metadata_destination_directory, expected_filename)
    assert file.size == image_with_metadata_filesize
    assert file.name_clash is True


def test_duplicate_files_are_marked_as_having_no_destination_filepath_and_not_having_name_clash():
    prepare_test_media_source_file()
    prepare_test_media_destination_duplicate_file()

    save_pre_copy_file_record(image_with_metadata_source_filepath)

    file = instantiate_file_from_db_record(image_with_metadata_source_filepath)

    assert file.source_filepath == image_with_metadata_source_filepath
    assert file.name_clash is False
    assert file.destination_filepath is None


def test_denotes_copy_not_yet_attempted_by_setting_copied_and_copy_attempted_to_false():
    prepare_test_media_source_file()

    save_pre_copy_file_record(image_with_metadata_source_filepath)

    file = instantiate_file_from_db_record(image_with_metadata_source_filepath)

    assert file.source_filepath == image_with_metadata_source_filepath
    assert file.copied is False
    assert file.copy_attempted is False
