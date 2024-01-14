import pytest

from test.helpers import file_instance


@pytest.fixture
def copied_media_file():
    return file_instance(source_filepath='/source/copied_file.jpeg',
                         destination_filepath='/destination/copied_file.jpeg',
                         media=True, copied=True, copy_attempted=True)


@pytest.fixture
def copied_misc_file():
    return file_instance(source_filepath='/source/misc_file.txt',
                         destination_filepath='/destination/misc_file.txt',
                         media=False, copied=True, copy_attempted=True)


@pytest.fixture
def different_source_same_destination_1():
    return file_instance(source_filepath='/source/this_source.jpg',
                         destination_filepath='/destination/same_dest.jpg')


@pytest.fixture
def different_source_same_destination_2():
    return file_instance(source_filepath='/source/that_source.jpg',
                         destination_filepath='/destination/same_dest.jpg')


@pytest.fixture
def duplicate_file():
    return file_instance(source_filepath='/source/duplicate_file',
                         destination_filepath=None)


@pytest.fixture
def failed_copy_media_file():
    return file_instance(source_filepath='/source/media.jpeg',
                         destination_filepath='/destination/media.jpeg',
                         media=True, copied=False, copy_attempted=True)


@pytest.fixture
def failed_copy_misc_file():
    return file_instance(source_filepath='/source/file.txt',
                         destination_filepath='/destination/file.txt',
                         media=False, copied=False, copy_attempted=True)


@pytest.fixture
def file():
    return file_instance(source_filepath='/source/file1.jpg',
                         destination_filepath='/destination/file1.jpg',
                         size=11)


@pytest.fixture
def file_2():
    return file_instance(source_filepath='/source/file2.jpg',
                         destination_filepath='/destination/file2.jpg',
                         size=5)


@pytest.fixture
def file_with_copy_error():
    return file_instance(source_filepath='/source/file_with_copy_error',
                         destination_filepath='/destination/file_with_copy_error',
                         copied=False, copy_attempted=True)


@pytest.fixture
def file_with_name_clash():
    return file_instance(source_filepath='/source/valid_name_clash_file',
                         destination_filepath='/destination/valid_name_clash_file',
                         name_clash=True)


@pytest.fixture
def not_to_copy():
    return file_instance(source_filepath='/source/file_with_copy_error',
                         destination_filepath=None, size=7)


@pytest.fixture
def same_source_different_destination_1():
    return file_instance(source_filepath='/source/same_source.jpg',
                         destination_filepath='/destination/this_dest.jpg')


@pytest.fixture
def same_source_different_destination_2():
    return file_instance(source_filepath='/source/same_source.jpg',
                         destination_filepath='/destination/that_dest.jpg')


@pytest.fixture
def uncopied_media_file():
    return file_instance(source_filepath='/source/file1.jpg',
                         destination_filepath='/destination/file1.jpg',
                         media=True, copied=False, copy_attempted=False, size=3)


@pytest.fixture
def uncopied_misc_file():
    return file_instance(source_filepath='/source/file.txt',
                         destination_filepath='/destination/file.txt',
                         media=False, copied=False, copy_attempted=False)


@pytest.fixture
def uncopied_file_2():
    return file_instance(source_filepath='/source/file2.jpg',
                         destination_filepath='/destination/file2.jpg',
                         copied=False, copy_attempted=False, size=5)
