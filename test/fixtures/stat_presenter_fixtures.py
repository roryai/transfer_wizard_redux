from test.helpers import *


@pytest.fixture
def simple_media_file_1():
    return file_instance(source_filepath='source/simple_media_file_1',
                         destination_filepath='destination/simple_media_file_1',
                         media=True, size=102400, name_clash=False)


@pytest.fixture
def simple_media_file_2():
    return file_instance(source_filepath='source/simple_media_file_2',
                         destination_filepath='destination/simple_media_file_2',
                         media=True, size=3276800, name_clash=False)


@pytest.fixture
def simple_misc_file_1():
    return file_instance(source_filepath='source/simple_misc_file_1',
                         destination_filepath='destination/simple_misc_file_1',
                         media=False, size=102400, name_clash=False)


@pytest.fixture
def duplicate_media_file_1():
    return file_instance(source_filepath='source/duplicate_media_file_1', media=True,
                         destination_filepath=None, size=204800, name_clash=False)


@pytest.fixture
def duplicate_media_file_2():
    return file_instance(source_filepath='source/duplicate_media_file_2', media=True,
                         destination_filepath=None, size=819200, name_clash=False)


@pytest.fixture
def name_clash_misc_file_1():
    return file_instance(source_filepath='source/name_clash_misc_file_1', media=False,
                         destination_filepath='destination/name_clash_file_1', size=1638400, name_clash=True)


@pytest.fixture
def name_clash_misc_file_2():
    return file_instance(source_filepath='source/name_clash_misc_file_2', media=False,
                         destination_filepath='destination/name_clash_file_2', size=409600, name_clash=True)
