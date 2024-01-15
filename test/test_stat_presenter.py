from .helpers import pytest, clear_db_and_test_directories, insert_db_record
from test.fixtures.stat_presenter_fixtures import *
from app.stat_presenter import StatPresenter


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_db_and_test_directories()


def present_stats():
    return StatPresenter('source/', 'destination/').print_stats_summary()


def test_plural_grammar_for_all_file_categories(capsys, simple_media_file_1, simple_media_file_2,
                                                duplicate_media_file_1, duplicate_media_file_2,
                                                name_clash_misc_file_1, name_clash_misc_file_2):
    expected_output = """Source root directory: source/
Destination root directory: destination/

6 candidate files discovered in source directory.
Total size of candidate files: 6.15MB

4 files are media files: 4.2MB
2 files are miscellaneous files: 1.95MB

2 files are duplicates and will not be copied.
2 files have name clashes and will be copied with a unique suffix.

4 files will be copied.
Total size of files to be copied: 5.18MB\n"""
    for f in [simple_media_file_1, simple_media_file_2, duplicate_media_file_1, duplicate_media_file_2, name_clash_misc_file_1, name_clash_misc_file_2]:
        insert_db_record(f)

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_singular_grammar_for_duplicate_and_name_clash_files(capsys, duplicate_media_file_1, name_clash_misc_file_1):
    expected_output = """Source root directory: source/
Destination root directory: destination/

2 candidate files discovered in source directory.
Total size of candidate files: 1.76MB

1 file is a media file: 0.2MB
1 file is a miscellaneous file: 1.56MB

1 file is a duplicate and will not be copied.
1 file has a name clash and will be copied with a unique suffix.

1 file will be copied.
Total size of file to be copied: 1.56MB\n"""
    for f in [duplicate_media_file_1, name_clash_misc_file_1]:
        insert_db_record(f)

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_singular_grammar_for_candidate_files_and_files_to_be_copied(capsys, simple_media_file_1):
    expected_output = """Source root directory: source/
Destination root directory: destination/

1 candidate file discovered in source directory.
Total size of candidate file: 0.1MB

1 file is a media file: 0.1MB

1 file will be copied.
Total size of file to be copied: 0.1MB\n"""
    insert_db_record(simple_media_file_1)

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_singular_grammar_for_candidate_misc_and_media_files(capsys, simple_media_file_1, simple_misc_file_1):
    expected_output = """Source root directory: source/
Destination root directory: destination/

2 candidate files discovered in source directory.
Total size of candidate files: 0.2MB

1 file is a media file: 0.1MB
1 file is a miscellaneous file: 0.1MB

2 files will be copied.
Total size of files to be copied: 0.2MB\n"""
    for f in [simple_media_file_1, simple_misc_file_1]:
        insert_db_record(f)

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_does_not_display_name_clash_or_duplicate_info_when_no_files_in_those_categories_are_present(
        capsys, simple_media_file_1, simple_media_file_2):
    expected_output = """Source root directory: source/
Destination root directory: destination/

2 candidate files discovered in source directory.
Total size of candidate files: 3.22MB

2 files are media files: 3.22MB

2 files will be copied.
Total size of files to be copied: 3.22MB\n"""
    for f in [simple_media_file_1, simple_media_file_2]:
        insert_db_record(f)

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_displays_no_files_found_message(capsys):
    expected_output = """Source root directory: source/
Destination root directory: destination/

No files found in source directory.\n"""

    present_stats()
    captured = capsys.readouterr()

    assert captured.out == expected_output
