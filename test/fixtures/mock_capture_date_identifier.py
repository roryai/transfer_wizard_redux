from datetime import datetime
import pytest

from app.capture_date_identifier import CaptureDateIdentifier


@pytest.fixture(autouse=True)
def mock_capture_date_identifier_metadata_readable(mocker):
    instance = CaptureDateIdentifier()

    desired_date = datetime(2023, 12, 3)
    mocker.patch.object(instance, 'media_capture_date',
                        return_value=({'capture_date': desired_date, 'metadata_unreadable': False}))
    return instance


@pytest.fixture(autouse=True)
def mock_capture_date_identifier_metadata_unreadable(mocker):
    instance = CaptureDateIdentifier()

    desired_date = datetime(2023, 12, 3)
    mocker.patch.object(instance, 'media_capture_date',
                        return_value=({'capture_date': desired_date, 'metadata_unreadable': True}))
    return instance
