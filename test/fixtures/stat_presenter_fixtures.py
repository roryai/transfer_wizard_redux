from test.helpers import *


@pytest.fixture
def simple_file_1():
    return file_instance(source_filepath='source/simple_file_1',
                         destination_filepath='destination/simple_file_1', size=102400, name_clash=False)


@pytest.fixture
def simple_file_2():
    return file_instance(source_filepath='source/simple_file_2',
                         destination_filepath='destination/simple_file_2', size=3276800, name_clash=False)


@pytest.fixture
def duplicate_file_1():
    return file_instance(source_filepath='source/duplicate_file_1',
                         destination_filepath=None, size=204800, name_clash=False)


@pytest.fixture
def duplicate_file_2():
    return file_instance(source_filepath='source/duplicate_file_2',
                         destination_filepath=None, size=819200, name_clash=False)


@pytest.fixture
def name_clash_file_1():
    return file_instance(source_filepath='source/name_clash_file_1',
                         destination_filepath='destination/name_clash_file_1', size=1638400, name_clash=True)


@pytest.fixture
def name_clash_file_2():
    return file_instance(source_filepath='source/name_clash_file_2',
                         destination_filepath='destination/name_clash_file_2', size=409600, name_clash=True)
