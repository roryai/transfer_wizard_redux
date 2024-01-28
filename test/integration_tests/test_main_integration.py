from datetime import date
import os
from pathlib import Path
import shutil
from test.helpers import (pytest, cleanup, construct_path, create_file_on_disk, destination_root_directory,
                          misc_destination_root_directory, source_directory)
from test.fixtures.main_fixtures import set_copy_media_args, set_copy_all_filetypes_args

from main import main
from app.logger import Logger


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


photo_filename = 'DSC02204.JPG'
video_filename = 'IMG_3639_HEVC.MOV'
misc_filename = 'file.gif'
home_directory = os.path.expanduser("~")
this_year = str(date.today().year)
expected_destination_photo_file_path = construct_path(destination_root_directory, '2017/Q2', photo_filename)
expected_destination_video_file_path = construct_path(destination_root_directory, '2019/Q3', video_filename)
expected_destination_misc_file_path = construct_path(misc_destination_root_directory, this_year, misc_filename)


def prepare_test_resources():
    nested_directory = construct_path(source_directory, 'nest')
    Path(nested_directory).mkdir(parents=True, exist_ok=True)
    # misc file can be empty as metadata isn't read
    create_file_on_disk(nested_directory, 'file.gif')
    photo_filepath = \
        f'{home_directory}/code/transfer_wizard_redux/test/test_resources/static_media/{photo_filename}'
    video_filepath = \
        f'{home_directory}/code/transfer_wizard_redux/test/test_resources/static_media/{video_filename}'
    # real photo and video required so that metadata can be read
    for path in [photo_filepath, video_filepath]:
        shutil.copy2(path, source_directory)


media_and_misc_copy_expected_logfile_contents = f"""Source root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/source
Destination root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/destination

        Discovered         To be copied       Duplicate          Name clash
        Count   Size       Count   Size       Count   Size       Count   Size
______________________________________________________________________________
Media   2       8.74MB     2       8.74MB     0       0.0MB      0       0.0MB      
Misc    1       0.0MB      1       0.0MB      0       0.0MB      0       0.0MB      
______________________________________________________________________________
Total   3       8.74MB     3       8.74MB     0       0.0MB      0       0.0MB      

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
3 files
8.74MB

Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{photo_filename} copied to {expected_destination_photo_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{video_filename} copied to {expected_destination_video_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/nest/file.gif copied to {expected_destination_misc_file_path}

3 files copied successfully
0 files failed to copy

Errors:

"""

media_only_copy_expected_logfile_contents = f"""Source root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/source
Destination root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/destination

        Discovered         To be copied       Duplicate          Name clash
        Count   Size       Count   Size       Count   Size       Count   Size
______________________________________________________________________________
Media   2       8.74MB     2       8.74MB     0       0.0MB      0       0.0MB      
Misc    0       0.0MB      0       0.0MB      0       0.0MB      0       0.0MB      
______________________________________________________________________________
Total   2       8.74MB     2       8.74MB     0       0.0MB      0       0.0MB      

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
2 files
8.74MB

Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{photo_filename} copied to {expected_destination_photo_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{video_filename} copied to {expected_destination_video_file_path}

2 files copied successfully
0 files failed to copy

Errors:

"""


def test_happy_path_of_media_and_misc_copy(monkeypatch, set_copy_all_filetypes_args):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    prepare_test_resources()

    main()

    assert Path(expected_destination_photo_file_path).is_file()
    assert Path(expected_destination_video_file_path).is_file()
    assert Path(expected_destination_misc_file_path).is_file()

    with open(Logger().log_file_path, 'r') as file:
        contents = file.read()
        assert contents == media_and_misc_copy_expected_logfile_contents


def test_happy_path_of_media_only_copy(monkeypatch, set_copy_media_args):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    prepare_test_resources()

    main()

    assert Path(expected_destination_photo_file_path).is_file()
    assert Path(expected_destination_video_file_path).is_file()
    assert not Path(expected_destination_misc_file_path).is_file()

    with open(Logger().log_file_path, 'r') as file:
        contents = file.read()
        assert contents == media_only_copy_expected_logfile_contents
