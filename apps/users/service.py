from apps.users.serializers import CustomUserSerializer
from apps.users.repository import UserRepository
from apps.invite_codes.serializers import (
    InviteCodeSerializer,
    InviteCodeActivationSerializer
)


class UserService:
    def get_profile(
            self,
            user_id: int
    ) -> CustomUserSerializer:
        return UserRepository().get_profile(
            user_id=user_id
        )

    def active_invite_code(
            self,
            user_id: int,
            invite_code: InviteCodeActivationSerializer
    ) -> InviteCodeSerializer:
        return UserRepository().active_invite_code(
            user_id=user_id,
            invite_code=invite_code
        )
