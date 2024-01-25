import os
from pathlib import Path
from test.helpers import (pytest, cleanup, construct_path, create_file_on_disk, destination_root_directory,
                          misc_destination_directory, source_directory)
from test.fixtures.main_fixtures import set_copy_media_args, set_copy_all_filetypes_args

from main import main
from app.logger import Logger


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


media_filename = 'file.jpg'
misc_filename = 'file.gif'


def prepare_test_resources():
    nested_directory = construct_path(source_directory, 'nest')
    Path(nested_directory).mkdir(parents=True, exist_ok=True)
    media_source_filepath = create_file_on_disk(source_directory, media_filename)
    misc_source_filepath = create_file_on_disk(nested_directory, 'file.gif')

    time_in_past = 1701639908  # 03/12/23
    # set mtime (and atime) to past so destination directory structure is predictable
    os.utime(media_source_filepath, (time_in_past, time_in_past))

    return media_source_filepath, misc_source_filepath


expected_destination_media_file_path = destination_root_directory + f'/2023/{media_filename}'
expected_destination_misc_file_path = misc_destination_directory + f'/{misc_filename}'
home_directory = os.path.expanduser("~")

media_and_misc_copy_expected_logfile_contents = f"""Source root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/source
Destination root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/destination

        Discovered         To be copied       Duplicate          Name clash
        Count   Size       Count   Size       Count   Size       Count   Size
______________________________________________________________________________
Media   1       0.0MB      1       0.0MB      0       0.0MB      0       0.0MB      
Misc    1       0.0MB      1       0.0MB      0       0.0MB      0       0.0MB      
______________________________________________________________________________
Total   2       0.0MB      2       0.0MB      0       0.0MB      0       0.0MB      

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
2 files
0.0MB

Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/file.jpg copied to /Users/rory/code/transfer_wizard_redux/test/test_resources/destination/2023/file.jpg
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/nest/file.gif copied to /Users/rory/code/transfer_wizard_redux/test/test_resources/destination/misc/file.gif

2 files copied successfully
0 files failed to copy

Errors:

"""

media_only_copy_expected_logfile_contents = f"""Source root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/source
Destination root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/destination

        Discovered         To be copied       Duplicate          Name clash
        Count   Size       Count   Size       Count   Size       Count   Size
______________________________________________________________________________
Media   1       0.0MB      1       0.0MB      0       0.0MB      0       0.0MB      
Misc    0       0.0MB      0       0.0MB      0       0.0MB      0       0.0MB      
______________________________________________________________________________
Total   1       0.0MB      1       0.0MB      0       0.0MB      0       0.0MB      

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
1 file
0.0MB

Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/file.jpg copied to /Users/rory/code/transfer_wizard_redux/test/test_resources/destination/2023/file.jpg

1 file copied successfully
0 files failed to copy

Errors:

"""


def test_happy_path_of_media_and_misc_copy(monkeypatch, set_copy_all_filetypes_args):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    media_source_filepath, misc_source_filepath = prepare_test_resources()

    main()

    assert Path(media_source_filepath).is_file()
    assert Path(misc_source_filepath).is_file()
    assert Path(expected_destination_media_file_path).is_file()
    assert Path(expected_destination_misc_file_path).is_file()

    with open(Logger().log_file_path, 'r') as file:
        contents = file.read()
        assert contents == media_and_misc_copy_expected_logfile_contents


def test_happy_path_of_media_only_copy(monkeypatch, set_copy_media_args):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    media_source_filepath, misc_source_filepath = prepare_test_resources()

    main()

    assert Path(media_source_filepath).is_file()
    assert Path(misc_source_filepath).is_file()
    assert Path(expected_destination_media_file_path).is_file()
    assert not Path(expected_destination_misc_file_path).is_file()

    with open(Logger().log_file_path, 'r') as file:
        contents = file.read()
        assert contents == media_only_copy_expected_logfile_contents
