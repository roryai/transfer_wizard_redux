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
______________________________________________________________________________
Media   0       0.0MB      0       0.0MB      0       0.0MB      0       0.0MB      
Misc    0       0.0MB      0       0.0MB      0       0.0MB      0       0.0MB      
______________________________________________________________________________
Total   0       0.0MB      0       0.0MB      0       0.0MB      0       0.0MB      

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
0 files
0.0MB

"""

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_summary_and_table_output_with_data(capsys, uncopied_media_file, uncopied_misc_file,
                                            duplicate_media_file, duplicate_misc_file,
                                            media_file_with_name_clash, misc_file_with_name_clash):
    expected_output = """Source root directory: source/
Destination root directory: destination/

        Discovered         To be copied       Duplicate          Name clash
        Count   Size       Count   Size       Count   Size       Count   Size
______________________________________________________________________________
Media   3       101.0MB    2       90.0MB     1       11.0MB     1       37.0MB     
Misc    3       115.0MB    2       102.0MB    1       13.0MB     1       41.0MB     
______________________________________________________________________________
Total   6       216.0MB    4       192.0MB    2       24.0MB     2       78.0MB     

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
4 files
192.0MB

"""
    for f in [uncopied_media_file, uncopied_misc_file,
              duplicate_media_file, duplicate_misc_file,
              media_file_with_name_clash, misc_file_with_name_clash]:
        insert_db_record(f)

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output
