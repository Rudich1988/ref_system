from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.authentication.models import PhoneAuth


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=12,
        min_length=11,
        help_text='+79251353782',
        required=True
    )

    def validate_phone_number(self, value):
        if not (value.startswith('+7') or value.startswith('8')):
            raise ValidationError(
                "The phone number must start with '+7' or '8'"
            )
        return value

class PhoneAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneAuth
        fields = [
            'id',
            'phone_number',
            'code',
            'created_at',
            'expires_at'
        ]
        read_only_fields = ['id', 'created_at', 'expires_at']


class PhoneCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=12,
        min_length=11,
        help_text='+79251353782',
        required=True
    )
    code = serializers.CharField(
        max_length=4,
        min_length=4,
        required=True,
        help_text='1234'
    )

    def validate_phone_number(self, value):
        if not (value.startswith('+7') or value.startswith('8')):
            raise ValidationError(
                "The phone number must start with '+7' or '8'"
            )
        return value


class TokensSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=4, max_length=4)
