from .helpers import (pytest, cleanup, construct_path, create_test_misc_files, destination_root_directory,
                      image_with_metadata_source_filepath, instantiate_file_from_db_record,
                      prepare_test_media_destination_name_clash_file, image_with_metadata_destination_directory,
                      prepare_test_media_source_file, prepare_test_media_destination_duplicate_file)
from app.file_factory import FileFactory


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def save_pre_copy_file_record(source_filepath, media):
    FileFactory(source_filepath, destination_root_directory).save_pre_copy_file_record(media)


def test_a_media_file_is_built_and_saved():
    destination_filepath = prepare_test_media_source_file()

    save_pre_copy_file_record(image_with_metadata_source_filepath, media=True)

    file = instantiate_file_from_db_record(image_with_metadata_source_filepath)

    assert file.source_filepath == image_with_metadata_source_filepath
    assert file.destination_filepath == destination_filepath
    assert file.size == 195514
    assert file.name_clash is False
    assert file.copied is False
    assert file.media is True


def test_a_misc_file_is_built_and_saved():
    source_data = 'this_string_is_23_bytes'
    _, source_filepath, _, destination_filepath = create_test_misc_files(
        source_data=source_data)

    save_pre_copy_file_record(source_filepath, media=False)

    file = instantiate_file_from_db_record(source_filepath)

    assert file.source_filepath == source_filepath
    assert file.destination_filepath == destination_filepath
    assert file.size == 23
    assert file.name_clash is False
    assert file.copied is False
    assert file.media is False


def test_file_is_marked_as_having_name_clash_when_an_existing_destination_file_has_same_name_and_different_size():
    prepare_test_media_source_file()
    prepare_test_media_destination_name_clash_file()

    save_pre_copy_file_record(image_with_metadata_source_filepath, media=True)

    file = instantiate_file_from_db_record(image_with_metadata_source_filepath)
    expected_filename = 'IMG_1687_68E3___1.jpg'

    assert file.source_filepath == image_with_metadata_source_filepath
    assert file.destination_filepath == construct_path(image_with_metadata_destination_directory, expected_filename)
    assert file.size == 195514
    assert file.name_clash is True


def test_duplicate_files_are_marked_as_having_no_destination_filepath_and_not_having_name_clash():
    prepare_test_media_source_file()
    prepare_test_media_destination_duplicate_file()

    save_pre_copy_file_record(image_with_metadata_source_filepath, media=True)

    file = instantiate_file_from_db_record(image_with_metadata_source_filepath)

    assert file.source_filepath == image_with_metadata_source_filepath
    assert file.name_clash is False
    assert file.destination_filepath is None


def test_denotes_copy_not_yet_attempted_by_setting_copied_and_copy_attempted_to_false():
    prepare_test_media_source_file()

    save_pre_copy_file_record(image_with_metadata_source_filepath, media=True)

    file = instantiate_file_from_db_record(image_with_metadata_source_filepath)

    assert file.source_filepath == image_with_metadata_source_filepath
    assert file.copied is False
    assert file.copy_attempted is False
