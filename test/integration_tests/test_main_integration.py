from test.helpers import cleanup
from test.fixtures.main_fixtures import set_default_copy_args, set_year_mode_args
from test.fixtures.main_integration_fixtures import *

from main import main
from app.logger import Logger


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def test_year_mode_happy_path_file_creation(prepare_test_resources, set_year_mode_args):
    main()

    assert Path(year_mode_expected_destination_jpg_file_path).is_file()
    assert Path(year_mode_expected_destination_raf_file_path).is_file()
    assert Path(year_mode_expected_destination_video_file_path).is_file()


def test_year_mode_happy_path_log_output(prepare_test_resources, set_year_mode_args):
    main()

    with open(Logger().log_file_path, 'r') as file:
        contents = file.read()

    assert contents.startswith(
        f"""Source root directory: {source_root_directory}
Destination root directory: {destination_root_directory}

Discovered         To be copied       Duplicate          Name clash
Count   Size       Count   Size       Count   Size       Count   Size
____________________________________________________________________________
3       75.52MB    3       75.52MB    0       0.0MB      0       0.0MB      

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
3 files
75.52MB
"""
    )

    expected_success_lines = [
        f"Copy succeeded: {source_root_directory / raf_filename} copied to {year_mode_expected_destination_raf_file_path}",
        f"Copy succeeded: {source_root_directory / jpg_filename} copied to {year_mode_expected_destination_jpg_file_path}",
        f"Copy succeeded: {source_root_directory / video_filename} copied to {year_mode_expected_destination_video_file_path}",
    ]

    for line in expected_success_lines:
        assert line in contents, f"Expected success line not found: {line}"

    # --- Check footer ---
    assert """3 files copied successfully
0 files failed to copy
Errors:""" in contents


def test_default_mode_happy_path(media_only_copy_expected_logfile_contents, set_default_copy_args):
    main()

    assert Path(default_mode_expected_destination_jpg_file_path).is_file()
    assert Path(default_mode_expected_destination_raf_file_path).is_file()
    assert Path(default_mode_expected_destination_video_file_path).is_file()


def test_default_mode_happy_path_log_output(prepare_test_resources, set_default_copy_args):
    main()

    with open(Logger().log_file_path, 'r') as file:
        contents = file.read()

    assert contents.startswith(
        f"""Source root directory: {source_root_directory}
Destination root directory: {destination_root_directory}

Discovered         To be copied       Duplicate          Name clash
Count   Size       Count   Size       Count   Size       Count   Size
____________________________________________________________________________
3       75.52MB    3       75.52MB    0       0.0MB      0       0.0MB      

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
3 files
75.52MB
"""
    )

    expected_success_lines = [
        f"Copy succeeded: {source_root_directory / raf_filename} copied to {default_mode_expected_destination_raf_file_path}",
        f"Copy succeeded: {source_root_directory / jpg_filename} copied to {default_mode_expected_destination_jpg_file_path}",
        f"{source_root_directory / video_filename} copied to {default_mode_expected_destination_video_file_path}",
    ]

    for line in expected_success_lines:
        assert line in contents, f"Expected success line not found: {line}"

    # --- Check footer ---
    assert """3 files copied successfully
0 files failed to copy
Errors:""" in contents
