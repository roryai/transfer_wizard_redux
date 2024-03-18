from datetime import date, datetime
from test.helpers import (pytest, construct_path, cleanup, create_file_on_disk,
                          create_test_misc_files, destination_root_directory, static_media_directory)
from app.capture_time_identifier import CaptureTimeIdentifier
from test.fixtures.capture_time_identifier_fixtures import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def class_under_test():
    return CaptureTimeIdentifier()


def earliest_file_system_date(filepath):
    return class_under_test()._earliest_file_system_date(filepath)['capture_date']


def approximate_file_creation_date(filepath):
    return class_under_test().approximate_file_creation_date(filepath)['capture_date']


def test_identifies_capture_time_for_jpeg_from_sony_camera():
    photo_path = construct_path(static_media_directory, 'DSC02204.JPG')
    metadata_date = approximate_file_creation_date(photo_path)
    expected_date = datetime.strptime('3 June 2017', "%d %B %Y").date()

    assert metadata_date == expected_date


def test_identifies_capture_time_for_jpg_from_iphone():
    photo_path = construct_path(static_media_directory, 'IMG_1687_68E3.jpg')
    metadata_date = approximate_file_creation_date(photo_path)
    expected_date = datetime.strptime('11 September 2018', "%d %B %Y").date()

    assert metadata_date == expected_date


def test_identifies_capture_time_for_heic_photo():
    photo_path = construct_path(static_media_directory, 'IMG_1263.HEIC')
    metadata_date = approximate_file_creation_date(photo_path)
    expected_date = datetime.strptime('21 June 2018', "%d %B %Y").date()

    assert metadata_date == expected_date


def test_identifies_capture_time_for_hevc_mov_video():
    video_path = construct_path(static_media_directory, 'IMG_3639_HEVC.MOV')
    metadata_date = approximate_file_creation_date(video_path)
    expected_date = datetime.strptime('27 August 2019', "%d %B %Y").date()

    assert metadata_date == expected_date


def test_identifies_capture_time_for_mp4_video():
    video_path = construct_path(static_media_directory, 'C0001.MP4')
    metadata_date = approximate_file_creation_date(video_path)
    expected_date = datetime.strptime('25 May 2017', "%d %B %Y").date()

    assert metadata_date == expected_date


def test_identifies_capture_time_for_h264_video():
    video_path = construct_path(static_media_directory, '00029.MTS')
    metadata_date = approximate_file_creation_date(video_path)
    expected_date = datetime.strptime('25 May 2017', "%d %B %Y").date()

    assert metadata_date == expected_date


def test_identifies_capture_time_for_avi_video():
    video_path = construct_path(static_media_directory, 'MVI_2227.AVI')
    metadata_date = approximate_file_creation_date(video_path)
    expected_date = datetime.strptime('27 July 2012', "%d %B %Y").date()

    assert metadata_date == expected_date


def test_identifies_capture_time_for_wmv_video():
    video_path = construct_path(static_media_directory, '019.wmv')
    metadata_date = approximate_file_creation_date(video_path)
    expected_date = datetime.strptime('3 April 2009', "%d %B %Y").date()

    assert metadata_date == expected_date


def test_identifies_capture_time_for_m2ts_video():
    video_path = construct_path(static_media_directory, '20160802141815.m2ts')
    metadata_date = approximate_file_creation_date(video_path)
    expected_date = datetime.strptime('2 August 2016', "%d %B %Y").date()

    assert metadata_date == expected_date


def test_identifies_capture_time_for_mov_video():
    video_path = construct_path(static_media_directory, 'ski.mov')
    metadata_date = approximate_file_creation_date(video_path)
    expected_date = datetime.strptime('18 January 2008', "%d %B %Y").date()

    assert metadata_date == expected_date


def test_defaults_to_file_system_dates_for_misc_file():
    misc_filepath = create_file_on_disk(destination_root_directory, 'file.gif')
    system_file_info_date = approximate_file_creation_date(misc_filepath)
    expected_date = date.today()

    assert system_file_info_date == expected_date


def test_logs_info_when_metadata_read_of_media_files_fails():
    # this file has unreadable metadata
    video_path = construct_path(static_media_directory, 'MOV02021.MPG')
    system_file_info_date = approximate_file_creation_date(video_path)
    expected_date = datetime.strptime('27 January 2024', "%d %B %Y").date()

    assert system_file_info_date == expected_date


def test_uses_birth_time_for_capture_time_when_it_is_earliest_file_stat_time(birth_time_first):
    generated_date = earliest_file_system_date('this_string_satisfies_mocked_Path')
    expected_date = datetime.fromtimestamp(birth_time_first.st_birthtime).date()

    assert expected_date == generated_date


def test_uses_modified_time_for_capture_time_when_it_is_earliest_file_stat_time(modified_time_first):
    generated_date = earliest_file_system_date('this_string_satisfies_mocked_Path')
    expected_date = datetime.fromtimestamp(modified_time_first.st_mtime).date()

    assert expected_date == generated_date


def test_uses_creation_time_for_capture_time_when_it_is_earliest_file_stat_time(creation_time_first):
    generated_date = earliest_file_system_date('this_string_satisfies_mocked_Path')
    expected_date = datetime.fromtimestamp(creation_time_first.st_ctime).date()

    assert expected_date == generated_date


def test_unreadable_photo_metadata_recorded_in_result():
    _, filepath, _, _ = create_test_misc_files()
    result = class_under_test()._get_date_taken_for_photo(filepath)
    expected_date = datetime.strptime('3 December 2023', "%d %B %Y").date()

    assert result == ({'capture_date': expected_date, 'metadata_unreadable': True})


def test_unreadable_video_metadata_recorded_in_result():
    _, filepath, _, _ = create_test_misc_files()
    result = class_under_test()._get_date_taken_for_video(filepath)
    expected_date = datetime.strptime('3 December 2023', "%d %B %Y").date()

    assert result == ({'capture_date': expected_date, 'metadata_unreadable': True})


def test_readable_photo_metadata_recorded_in_result():
    photo_path = construct_path(static_media_directory, 'DSC02204.JPG')
    result = class_under_test()._get_date_taken_for_photo(photo_path)
    expected_date = datetime.strptime('3 June 2017', "%d %B %Y").date()

    assert result == ({'capture_date': expected_date, 'metadata_unreadable': False})


def test_readable_video_metadata_recorded_in_result():
    video_path = construct_path(static_media_directory, 'IMG_3639_HEVC.MOV')
    result = class_under_test()._get_date_taken_for_video(video_path)
    expected_date = datetime.strptime('27 August 2019', "%d %B %Y").date()

    assert result == ({'capture_date': expected_date, 'metadata_unreadable': False})
