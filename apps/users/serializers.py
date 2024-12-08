from rest_framework import serializers
from rest_framework.serializers import ValidationError

from apps.invite_codes.models import InviteCode
from apps.users.models import CustomUser


class UserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=12,
        required=False
    )
    invite_code = serializers.CharField(
        max_length=6,
        required=False
    )

    def validate(self, data):
        if not data.get(
                'phone_number'
        ) and not data.get('invite_code'):
            raise ValidationError(
                'Either phone_number or invite_code is required.'
            )
        return data


class UserModelSerializer(serializers.ModelSerializer):
    invite_code = serializers.PrimaryKeyRelatedField(
        queryset=InviteCode.objects.all(),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'phone_number',
            'created_at',
            'activated_invite_code',
            'invite_code'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'activated_invite_code',
        ]


class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    phone_number = serializers.CharField(
        max_length=12,
        min_length=12
    )
    invite_code = serializers.CharField(
        max_length=6,
        min_length=6
    )
    activated_invite_code = serializers.CharField(
        max_length=6,
        min_length=6,
        required=False,
        allow_null=True
    )
    referred_users_phone_numbers = serializers.ListField(
        child=serializers.CharField(
            max_length=12,
            min_length=12
        ),
        allow_empty=True
    )
