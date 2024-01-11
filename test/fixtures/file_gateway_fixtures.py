from test.helpers import *


@pytest.fixture
def file():
    return file_instance(source_filepath='/source/file1.jpg', destination_filepath='/destination/file1.jpg')


@pytest.fixture
def file_2():
    return file_instance(source_filepath='/source/file2.jpg', destination_filepath='/destination/file2.jpg')


@pytest.fixture
def copied_file():
    return file_instance(source_filepath='/source/copied_file',
                         destination_filepath='/destination/copied_file')


@pytest.fixture
def file_with_copy_error():
    return file_instance(source_filepath='/source/file_with_copy_error',
                         destination_filepath='/destination/file_with_copy_error')


@pytest.fixture
def file_with_name_clash():
    return file_instance(source_filepath='/source/valid_name_clash_file',
                         destination_filepath='/destination/valid_name_clash_file',
                         name_clash=True)


@pytest.fixture
def duplicate_file():
    return file_instance(source_filepath='/source/duplicate_file',
                         destination_filepath=None)


@pytest.fixture
def to_be_copied_1():
    return file_instance(source_filepath='/source/copy_candidate',
                         destination_filepath='/destination/copy_candidate',
                         size=1024)


@pytest.fixture
def to_be_copied_2():
    return file_instance(source_filepath='/source/copy_candidate2',
                         destination_filepath='/destination/copy_candidate2', size=2048)


@pytest.fixture
def not_to_copy():
    return file_instance(source_filepath='/source/file_with_copy_error',
                         destination_filepath=None, size=10)


@pytest.fixture
def same_source_different_destination_1():
    return file_instance(source_filepath='/source/same_source.jpg',
                         destination_filepath='/destination/this_dest.jpg')


@pytest.fixture
def same_source_different_destination_2():
    return file_instance(source_filepath='/source/same_source.jpg',
                         destination_filepath='/destination/that_dest.jpg')


@pytest.fixture
def different_source_same_destination_1():
    return file_instance(source_filepath='/source/this_source.jpg',
                         destination_filepath='/destination/same_dest.jpg')


@pytest.fixture
def different_source_same_destination_2():
    return file_instance(source_filepath='/source/that_source.jpg',
                         destination_filepath='/destination/same_dest.jpg')
