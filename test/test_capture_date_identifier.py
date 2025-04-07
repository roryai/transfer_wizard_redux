from datetime import datetime
from test.helpers import (pytest, construct_path, cleanup, static_media_directory)
from app.capture_date_identifier import CaptureDateIdentifier


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def test_identifies_capture_date_for_jpg():
    photo_path = construct_path(static_media_directory, 'RRY01936.JPG')
    file_date = CaptureDateIdentifier().media_capture_date(photo_path)
    expected_date = datetime.strptime('1 April 2025', "%d %B %Y").date()

    assert file_date == expected_date


def test_identifies_capture_date_for_raw_file():
    photo_path = construct_path(static_media_directory, 'RRY01936.RAF')
    file_date = CaptureDateIdentifier().media_capture_date(photo_path)
    expected_date = datetime.strptime('1 April 2025', "%d %B %Y").date()

    assert file_date == expected_date


def test_identifies_capture_date_for_mov_video():
    video_path = construct_path(static_media_directory, 'RRY01937.MOV')
    file_date = CaptureDateIdentifier().media_capture_date(video_path)
    expected_date = datetime.strptime('1 April 2025', "%d %B %Y").date()

    assert file_date == expected_date
