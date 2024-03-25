from datetime import datetime
import pytest

from app.capture_time_identifier import CaptureTimeIdentifier, CaptureTimeIdentifierMeta


@pytest.fixture(autouse=True)
def mock_capture_time_identifier_metadata_readable(mocker):
    CaptureTimeIdentifierMeta._instance = {}
    instance = CaptureTimeIdentifier()

    desired_date = datetime(2023, 12, 3)
    mocker.patch.object(instance, 'approximate_file_creation_date',
                        return_value=({'capture_date': desired_date, 'metadata_unreadable': False}))
    return instance


@pytest.fixture(autouse=True)
def mock_capture_time_identifier_metadata_unreadable(mocker):
    CaptureTimeIdentifierMeta._instance = {}
    instance = CaptureTimeIdentifier()

    desired_date = datetime(2023, 12, 3)
    mocker.patch.object(instance, 'approximate_file_creation_date',
                        return_value=({'capture_date': desired_date, 'metadata_unreadable': True}))
    return instance
