from datetime import date
from pathlib import Path
import shutil

from test.helpers import (pytest, construct_path, source_directory)
from app.mode_flags import ModeFlagsMeta

BASE_DIR = Path(__file__).resolve().parent.parent
static_media_directory = BASE_DIR / 'test_resources' / 'static_media'
source_root_directory = BASE_DIR / 'test_resources' / 'source'
destination_root_directory = BASE_DIR / 'test_resources' / 'destination'

jpg_filename = 'RRY01936.JPG'
raf_filename = 'RRY01936.RAF'
video_filename = 'RRY01937.MOV'

this_year = str(date.today().year)

default_mode_expected_destination_jpg_file_path = construct_path(destination_root_directory, '2025/Q2', jpg_filename)
default_mode_expected_destination_raf_file_path = construct_path(destination_root_directory, '2025/Q2', raf_filename)
default_mode_expected_destination_video_file_path = construct_path(destination_root_directory, '2025/Q2', video_filename)

year_mode_expected_destination_jpg_file_path = construct_path(destination_root_directory, '2025', jpg_filename)
year_mode_expected_destination_raf_file_path = construct_path(destination_root_directory, '2025', raf_filename)
year_mode_expected_destination_video_file_path = construct_path(destination_root_directory, '2025', video_filename)


@pytest.fixture(autouse=True)
def prepare_test_resources(monkeypatch):
    ModeFlagsMeta._instance = {}
    monkeypatch.setattr('builtins.input', lambda: 'y')

    nested_directory = construct_path(source_directory, 'nest')
    Path(nested_directory).mkdir(parents=True, exist_ok=True)

    for filename in [jpg_filename, raf_filename, video_filename]:
        shutil.copy2(static_media_directory / filename, source_directory)


@pytest.fixture
def year_mode_expected_logfile_contents():
    return f"""Source root directory: {source_root_directory}
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

Copy succeeded: {source_root_directory / raf_filename} copied to {year_mode_expected_destination_raf_file_path}
Copy succeeded: {source_root_directory / jpg_filename} copied to {year_mode_expected_destination_jpg_file_path}
Copy succeeded: {source_root_directory / video_filename} copied to {year_mode_expected_destination_video_file_path}

3 files copied successfully
0 files failed to copy
Errors:

"""


@pytest.fixture
def media_only_copy_expected_logfile_contents():
    return f"""Source root directory: {source_root_directory}
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

Copy succeeded: {source_root_directory / raf_filename} copied to {default_mode_expected_destination_raf_file_path}
Copy succeeded: {source_root_directory / jpg_filename} copied to {default_mode_expected_destination_jpg_file_path}
Copy succeeded: {source_root_directory / video_filename} copied to {default_mode_expected_destination_video_file_path}

3 files copied successfully
0 files failed to copy
Errors:

"""
