from app.file import File
from app.stat_presenter import StatPresenter

from .helpers import *

simple_file_1 = file_instance(source_filepath='source/simple_file_1',
                              destination_filepath='destination/simple_file_1', size=102400, name_clash=False)
simple_file_2 = file_instance(source_filepath='source/simple_file_2',
                              destination_filepath='destination/simple_file_2', size=3276800, name_clash=False)
duplicate_file_1 = file_instance(source_filepath='source/duplicate_file_1',
                                 destination_filepath=None, size=204800, name_clash=False)
duplicate_file_2 = file_instance(source_filepath='source/duplicate_file_2',
                                 destination_filepath=None, size=819200, name_clash=False)
name_clash_file_1 = file_instance(source_filepath='source/name_clash_file_1',
                                  destination_filepath='destination/name_clash_file_1', size=1638400, name_clash=True)
name_clash_file_2 = file_instance(source_filepath='source/name_clash_file_2',
                                  destination_filepath='destination/name_clash_file_2', size=409600, name_clash=True)


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()
    clear_database()
    
    
def present_stats():
    return StatPresenter('source/', 'destination/').print_stats_summary()


def test_plural_grammar_for_all_file_categories(capsys):
    expected_output = """Source directory: source/
Destination directory: destination/

6 candidate files discovered in source directory.
Total size of candidate files: 6.15MB

2 files are duplicates and will not be copied.
2 files have name clashes and will be copied with a unique suffix.

4 files will be copied.
Total size of files to be copied: 5.18MB\n\n"""
    for f in [simple_file_1, simple_file_2, duplicate_file_1, duplicate_file_2, name_clash_file_1, name_clash_file_2]:
        insert_db_record(f)

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_singular_grammar_for_duplicate_and_name_clash_files(capsys):
    expected_output = """Source directory: source/
Destination directory: destination/

2 candidate files discovered in source directory.
Total size of candidate files: 1.76MB

1 file is a duplicate and will not be copied.
1 file has a name clash and will be copied with a unique suffix.

1 file will be copied.
Total size of file to be copied: 1.56MB\n\n"""
    for f in [duplicate_file_1, name_clash_file_1]:
        insert_db_record(f)

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_singular_grammar_for_candidate_files_and_files_to_be_copied(capsys):
    expected_output = """Source directory: source/
Destination directory: destination/

1 candidate file discovered in source directory.
Total size of candidate file: 0.1MB

1 file will be copied.
Total size of file to be copied: 0.1MB\n\n"""
    insert_db_record(simple_file_1)

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_does_not_display_name_clash_or_duplicate_info_when_no_files_in_these_categories_are_present(capsys):
    expected_output = """Source directory: source/
Destination directory: destination/

2 candidate files discovered in source directory.
Total size of candidate files: 3.22MB

2 files will be copied.
Total size of files to be copied: 3.22MB\n\n"""
    for f in [simple_file_1, simple_file_2]:
        insert_db_record(f)

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output
