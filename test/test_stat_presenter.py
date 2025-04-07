from .helpers import pytest, cleanup, insert_db_record
from test.fixtures.shared_fixtures import *
from app.stat_presenter import StatPresenter


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def present_stats():
    StatPresenter('source/', 'destination/').print_stats_summary()


def test_summary_and_table_output_blank_data(capsys):
    expected_output = """Source root directory: source/
Destination root directory: destination/

Discovered         To be copied       Duplicate          Name clash
Count   Size       Count   Size       Count   Size       Count   Size
____________________________________________________________________________
0       0.0MB      0       0.0MB      0       0.0MB      0       0.0MB      

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
0 files
0.0MB

"""

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_summary_and_table_output_with_data(capsys, uncopied_media_file,
                                            duplicate_media_file_1,
                                            media_file_with_name_clash):
    expected_output = """Source root directory: source/
Destination root directory: destination/

Discovered         To be copied       Duplicate          Name clash
Count   Size       Count   Size       Count   Size       Count   Size
____________________________________________________________________________
3       110.53MB   2       90.0MB     1       20.53MB    1       37.0MB     

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
2 files
90.0MB

"""
    for f in [uncopied_media_file, duplicate_media_file_1, media_file_with_name_clash]:
        insert_db_record(f)

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output
