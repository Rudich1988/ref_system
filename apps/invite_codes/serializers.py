from rest_framework import serializers

from apps.invite_codes.models import InviteCode


class InviteCodeSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = InviteCode
        fields = ['id', 'code', 'created_at']
        read_only_fields = ['id', 'created_at']


class InviteCodeActivationSerializer(
    serializers.Serializer
):
    code = serializers.CharField(max_length=6)
