from datetime import datetime
from test.helpers import (pytest, construct_path, cleanup, static_media_directory)
from app.capture_date_identifier import CaptureDateIdentifier


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def test_identifies_capture_date_for_jpeg():
    photo_path = construct_path(static_media_directory, 'RRY01936.JPG')
    file_date = CaptureDateIdentifier().media_capture_date(photo_path)['capture_date']
    expected_date = datetime.strptime('1 April 2025', "%d %B %Y").date()

    assert file_date == expected_date


def test_identifies_capture_date_for_raw_file():
    photo_path = construct_path(static_media_directory, 'RRY01936.RAF')
    file_date = CaptureDateIdentifier().media_capture_date(photo_path)['capture_date']
    expected_date = datetime.strptime('1 April 2025', "%d %B %Y").date()

    assert file_date == expected_date


def test_identifies_capture_date_for_mov_video():
    video_path = construct_path(static_media_directory, 'RRY01937.MOV')
    file_date = CaptureDateIdentifier().media_capture_date(video_path)['capture_date']
    expected_date = datetime.strptime('1 April 2025', "%d %B %Y").date()

    assert file_date == expected_date


def test_readable_photo_metadata_recorded_in_result():
    photo_path = construct_path(static_media_directory, 'RRY01507.JPG')
    result = CaptureDateIdentifier().media_capture_date(photo_path)
    expected_date = datetime.strptime('11 March 2025', "%d %B %Y").date()

    assert result == ({'capture_date': expected_date, 'metadata_unreadable': False})


def test_readable_video_metadata_recorded_in_result():
    video_path = construct_path(static_media_directory, 'RRY01856.MOV')
    result = CaptureDateIdentifier().media_capture_date(video_path)
    expected_date = datetime.strptime('27 March 2025', "%d %B %Y").date()

    assert result == ({'capture_date': expected_date, 'metadata_unreadable': False})
