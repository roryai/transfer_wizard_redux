from datetime import date
import os
from pathlib import Path
import shutil

from test.helpers import (pytest, construct_path, create_file_on_disk, destination_root_directory,
                          misc_destination_root_directory, source_directory)
from app.mode_flags import ModeFlagsMeta

photo_filename = 'DSC02204.JPG'
video_filename = 'IMG_3639_HEVC.MOV'
misc_filename = 'file.gif'
home_directory = os.path.expanduser("~")
this_year = str(date.today().year)
default_mode_expected_destination_photo_file_path = construct_path(destination_root_directory, '2017/Q2',
                                                                   photo_filename)
default_mode_expected_destination_video_file_path = construct_path(destination_root_directory, '2019/Q3',
                                                                   video_filename)
year_mode_expected_destination_photo_file_path = construct_path(destination_root_directory, '2017', photo_filename)
year_mode_expected_destination_video_file_path = construct_path(destination_root_directory, '2019', video_filename)
expected_destination_misc_file_path = construct_path(misc_destination_root_directory, this_year, misc_filename)


@pytest.fixture
def set_year_mode_args(monkeypatch):
    monkeypatch.setattr('sys.argv',
                        ['main.py', '-s', source_directory, '-d', destination_root_directory, '-y', '-misc'])


@pytest.fixture(autouse=True)
def prepare_test_resources(monkeypatch):
    ModeFlagsMeta._instance = {}
    monkeypatch.setattr('builtins.input', lambda: 'y')
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


@pytest.fixture
def default_mode_media_and_misc_copy_expected_logfile_contents():
    return f"""Source root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/source
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

Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{photo_filename} copied to {default_mode_expected_destination_photo_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{video_filename} copied to {default_mode_expected_destination_video_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/nest/file.gif copied to {expected_destination_misc_file_path}

3 files copied successfully
0 files failed to copy

Errors:

"""


@pytest.fixture
def year_mode_expected_logfile_contents():
    return f"""Source root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/source
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

Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{photo_filename} copied to {year_mode_expected_destination_photo_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{video_filename} copied to {year_mode_expected_destination_video_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/nest/file.gif copied to {expected_destination_misc_file_path}

3 files copied successfully
0 files failed to copy

Errors:

"""


@pytest.fixture
def media_only_copy_expected_logfile_contents():
    return f"""Source root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/source
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

Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{photo_filename} copied to {default_mode_expected_destination_photo_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{video_filename} copied to {default_mode_expected_destination_video_file_path}

2 files copied successfully
0 files failed to copy

Errors:

"""
