from rest_framework.exceptions import ValidationError
from typing_extensions import Optional

from apps.invite_codes.serializers import InviteCodeSerializer
from utils.repository import AbstractRepository

from apps.invite_codes.models import InviteCode


class InviteCodeRepository(AbstractRepository):
    def create(
            self,
            data: InviteCodeSerializer
    ) -> InviteCodeSerializer:
        try:
            data.is_valid(raise_exception=True)
            data = data.validated_data
            invite_code = InviteCode.objects.create(
                **data
            )
            return InviteCodeSerializer(
                invite_code
            )
        except ValidationError as e:
            raise e

    def get(
            self,
            code: InviteCodeSerializer
    ) -> Optional[InviteCodeSerializer]:
        code.is_valid(raise_exception=True)
        validate_data = code.validated_data
        invite_code = InviteCode.objects.filter(
            code=validate_data['code']
        ).first()
        if not invite_code:
            return None
        return InviteCodeSerializer(
            data={'code': invite_code}
        )
