from datetime import datetime
from test.helpers import pytest, cleanup
from app.capture_time_identifier import CaptureTimeIdentifier


@pytest.fixture
def teardown():
    cleanup()


def test_identifies_capture_time_for_jpeg_from_sony_camera():
    photo_path = '/Users/rory/code/transfer_wizard_redux/test/test_resources/static_pics/DSC02204.JPG'
    picture_date = CaptureTimeIdentifier().get_date_taken(photo_path)
    expected_date = datetime.strptime('3 June 2017', "%d %B %Y").date()

    assert picture_date == expected_date


def test_identifies_capture_time_for_iphone_photo():
    photo_path = '/Users/rory/code/transfer_wizard_redux/test/test_resources/static_pics/IMG_1687_68E3.jpg'
    picture_date = CaptureTimeIdentifier().get_date_taken(photo_path)
    expected_date = datetime.strptime('11 September 2018', "%d %B %Y").date()

    assert picture_date == expected_date


def test_identifies_capture_time_for_iphone_photo():
    photo_path = '/Users/rory/code/transfer_wizard_redux/test/test_resources/static_pics/IMG_1687_68E3.jpg'
    picture_date = CaptureTimeIdentifier().get_date_taken(photo_path)
    expected_date = datetime.strptime('11 September 2018', "%d %B %Y").date()

    assert picture_date == expected_date
