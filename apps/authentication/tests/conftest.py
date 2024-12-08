import pytest
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock

from services.verify_services.sms_verify_service import SmsVerifyService


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def mock_sms_service():
    with patch.object(
            SmsVerifyService,
            'create_code',
            return_value='1234'
    ) as mock:
        yield mock
