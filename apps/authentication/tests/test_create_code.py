import pytest
from unittest.mock import patch

from rest_framework.exceptions import ValidationError

from apps.authentication.serializers import PhoneNumberSerializer
from apps.authentication.services import AuthenticationService


@pytest.mark.django_db
@patch('services.verify_services.sms_verify_service.SmsVerifyService.create_code')
@patch('apps.authentication.repository.AuthenticationRepository.create')
def test_get_verify_code_valid_data(mock_create, mock_create_code):
    mock_create_code.return_value = '1234'
    data = {'phone_number': '+79251353782'}
    serializer = PhoneNumberSerializer(data=data)
    service = AuthenticationService()
    auth_code = service.get_verify_code(phone_data=serializer)

    assert auth_code == '1234'
    mock_create.assert_called_once()


@pytest.mark.django_db
@patch('services.verify_services.sms_verify_service.SmsVerifyService.create_code')
def test_get_verify_code_invalid_phone_number_short(mock_create_code):
    mock_create_code.return_value = '1234'
    data = {'phone_number': '1234567890'}
    serializer = PhoneNumberSerializer(data=data)
    service = AuthenticationService()

    with pytest.raises(ValidationError) as exc_info:
        service.get_verify_code(phone_data=serializer)
    assert 'phone_number' in exc_info.value.detail
    assert 'Ensure this field has at least 11 characters.' in str(
        exc_info.value.detail['phone_number'][0]
    )


@pytest.mark.django_db
@patch('services.verify_services.sms_verify_service.SmsVerifyService.create_code')
def test_get_verify_code_invalid_phone_number_long(mock_create_code):
    mock_create_code.return_value = '1234'
    data = {'phone_number': '12345678900000000000000'}
    serializer = PhoneNumberSerializer(data=data)
    service = AuthenticationService()

    with pytest.raises(ValidationError) as exc_info:
        service.get_verify_code(phone_data=serializer)
    assert 'phone_number' in exc_info.value.detail
    assert 'Ensure this field has no more than 12 characters.' in str(
        exc_info.value.detail['phone_number'][0]
    )


@pytest.mark.django_db
@patch('services.verify_services.sms_verify_service.SmsVerifyService.create_code')
def test_get_verify_code_invalid_phone_number_not_valid(mock_create_code):
    mock_create_code.return_value = '1234'
    data = {'phone_number': '+99261345643'}
    serializer = PhoneNumberSerializer(data=data)
    service = AuthenticationService()

    with pytest.raises(ValidationError) as exc_info:
        service.get_verify_code(phone_data=serializer)
    assert 'phone_number' in exc_info.value.detail
    assert "The phone number must start with '+7' or '8'" in str(
        exc_info.value.detail['phone_number'][0]
    )
