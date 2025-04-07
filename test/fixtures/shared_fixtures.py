import pytest

from test.helpers import file_instance


@pytest.fixture
def copied_media_file():
    return file_instance(source_filepath='/source/copied_file.jpeg',
                         destination_filepath='/destination/copied_file.jpeg',
                         copied=True, copy_attempted=True, size=2097152)


@pytest.fixture
def different_source_same_destination_1():
    return file_instance(source_filepath='/source/this_source.jpg',
                         destination_filepath='/destination/same_dest.jpg', size=5242880)


@pytest.fixture
def different_source_same_destination_2():
    return file_instance(source_filepath='/source/that_source.jpg',
                         destination_filepath='/destination/same_dest.jpg', size=7340032)


@pytest.fixture
def duplicate_media_file_1():
    return file_instance(source_filepath='/source/file_with_copy_error_1',
                         destination_filepath=None, size=21530000)


@pytest.fixture
def duplicate_media_file_2():
    return file_instance(source_filepath='/source/file_with_copy_error_2',
                         destination_filepath=None, size=11534336)


@pytest.fixture
def failed_copy_media_file():
    return file_instance(source_filepath='/source/media.jpeg',
                         destination_filepath='/destination/media.jpeg',
                         copied=False, copy_attempted=True, size=17825792)


@pytest.fixture
def file():
    return file_instance(source_filepath='/source/file1.jpg',
                         destination_filepath='/destination/file1.jpg',
                         size=24117248)


@pytest.fixture
def file_2():
    return file_instance(source_filepath='/source/file2.jpg',
                         destination_filepath='/destination/file2.jpg',
                         size=30408704)


@pytest.fixture
def file_with_copy_error():
    return file_instance(source_filepath='/source/file_with_copy_error',
                         destination_filepath='/destination/file_with_copy_error',
                         copied=False, copy_attempted=True, size=32017408)


@pytest.fixture
def media_file_with_name_clash():
    return file_instance(source_filepath='/source/valid_name_clash_file1',
                         destination_filepath='/destination/valid_name_clash_file1',
                         name_clash=True, size=38797312)


@pytest.fixture
def same_source_different_destination_1():
    return file_instance(source_filepath='/source/same_source.jpg',
                         destination_filepath='/destination/this_dest.jpg', size=45088768)


@pytest.fixture
def same_source_different_destination_2():
    return file_instance(source_filepath='/source/same_source.jpg',
                         destination_filepath='/destination/that_dest.jpg', size=49283072)


@pytest.fixture
def uncopied_media_file():
    return file_instance(source_filepath='/source/file1.jpg',
                         destination_filepath='/destination/file1.jpg',
                         copied=False, copy_attempted=False, size=55574528)


@pytest.fixture
def uncopied_media_file_2():
    return file_instance(source_filepath='/source/file2.jpg',
                         destination_filepath='/destination/file2.jpg',
                         copied=False, copy_attempted=False, size=61865984)
