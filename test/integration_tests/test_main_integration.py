from test.helpers import cleanup
from test.fixtures.main_fixtures import set_copy_media_args, set_copy_all_filetypes_args
from test.fixtures.main_integration_fixtures import *

from main import main
from app.logger import Logger


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def test_default_mode_happy_path_of_media_and_misc_copy(default_mode_media_and_misc_copy_expected_logfile_contents,
                                                        prepare_test_resources, set_copy_all_filetypes_args):
    main()

    assert Path(default_mode_expected_destination_photo_file_path).is_file()
    assert Path(default_mode_expected_destination_video_file_path).is_file()
    assert Path(expected_destination_misc_file_path).is_file()

    with open(Logger().log_file_path, 'r') as file:
        contents = file.read()
        assert contents == default_mode_media_and_misc_copy_expected_logfile_contents


def test_year_mode_happy_path_of_media_and_misc_copy(prepare_test_resources, set_year_mode_args,
                                                     year_mode_expected_logfile_contents):
    main()

    assert Path(year_mode_expected_destination_photo_file_path).is_file()
    assert Path(year_mode_expected_destination_video_file_path).is_file()
    assert Path(expected_destination_misc_file_path).is_file()

    with open(Logger().log_file_path, 'r') as file:
        contents = file.read()
        assert contents == year_mode_expected_logfile_contents


def test_happy_path_of_media_only_copy(media_only_copy_expected_logfile_contents,
                                       prepare_test_resources, set_copy_media_args):
    main()

    assert Path(default_mode_expected_destination_photo_file_path).is_file()
    assert Path(default_mode_expected_destination_video_file_path).is_file()
    assert not Path(expected_destination_misc_file_path).is_file()

    with open(Logger().log_file_path, 'r') as file:
        contents = file.read()
        assert contents == media_only_copy_expected_logfile_contents
