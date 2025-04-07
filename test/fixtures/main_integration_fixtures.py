from datetime import date
import os
from pathlib import Path
import shutil

from test.helpers import (pytest, construct_path, destination_root_directory, source_directory)
from app.mode_flags import ModeFlagsMeta

jpg_filename = 'RRY01936.JPG'
raf_filename = 'RRY01936.RAF'
video_filename = 'RRY01937.MOV'
home_directory = os.path.expanduser("~")
static_media_directory = '/code/transfer_wizard_redux/test/test_resources/static_media/'
this_year = str(date.today().year)
default_mode_expected_destination_jpg_file_path = construct_path(destination_root_directory, '2025/Q2',
                                                                 jpg_filename)
default_mode_expected_destination_raf_file_path = construct_path(destination_root_directory, '2025/Q2',
                                                                 raf_filename)
default_mode_expected_destination_video_file_path = construct_path(destination_root_directory, '2025/Q2',
                                                                   video_filename)
year_mode_expected_destination_jpg_file_path = construct_path(destination_root_directory, '2025', jpg_filename)
year_mode_expected_destination_raf_file_path = construct_path(destination_root_directory, '2025', raf_filename)
year_mode_expected_destination_video_file_path = construct_path(destination_root_directory, '2025', video_filename)


@pytest.fixture
def set_year_mode_args(monkeypatch):
    monkeypatch.setattr('sys.argv',
                        ['main.py', '-s', source_directory, '-d', destination_root_directory, '-y'])


@pytest.fixture(autouse=True)
def prepare_test_resources(monkeypatch):
    ModeFlagsMeta._instance = {}
    monkeypatch.setattr('builtins.input', lambda: 'y')
    nested_directory = construct_path(source_directory, 'nest')
    Path(nested_directory).mkdir(parents=True, exist_ok=True)
    jpg_filepath = \
        f'{home_directory}{static_media_directory}{jpg_filename}'
    raf_filepath = \
        f'{home_directory}{static_media_directory}{raf_filename}'
    video_filepath = \
        f'{home_directory}{static_media_directory}{video_filename}'
    # real photo and video required so that metadata can be read
    for path in [jpg_filepath, raf_filepath, video_filepath]:
        shutil.copy2(path, source_directory)


@pytest.fixture
def year_mode_expected_logfile_contents():
    return f"""Source root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/source
Destination root directory: {home_directory}/code/transfer_wizard_redux/test/test_resources/destination

Discovered         To be copied       Duplicate          Name clash
Count   Size       Count   Size       Count   Size       Count   Size
____________________________________________________________________________
3       75.52MB    3       75.52MB    0       0.0MB      0       0.0MB      

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
3 files
75.52MB

Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{raf_filename} copied to {year_mode_expected_destination_raf_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{jpg_filename} copied to {year_mode_expected_destination_jpg_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{video_filename} copied to {year_mode_expected_destination_video_file_path}

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
____________________________________________________________________________
3       75.52MB    3       75.52MB    0       0.0MB      0       0.0MB      

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
3 files
75.52MB

Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{raf_filename} copied to {default_mode_expected_destination_raf_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{jpg_filename} copied to {default_mode_expected_destination_jpg_file_path}
Copy succeeded: {home_directory}/code/transfer_wizard_redux/test/test_resources/source/{video_filename} copied to {default_mode_expected_destination_video_file_path}

3 files copied successfully
0 files failed to copy
Errors:

"""
