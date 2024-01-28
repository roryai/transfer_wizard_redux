from datetime import datetime
import pytest

from app.capture_time_identifier import CaptureTimeIdentifier


@pytest.fixture(autouse=True)
def mock_capture_time_identifier(mocker):
    original_instance = CaptureTimeIdentifier()

    desired_date = datetime(2023, 12, 3)
    mocker.patch.object(original_instance, 'approximate_file_creation_date',
                        return_value=desired_date)
    return original_instance
