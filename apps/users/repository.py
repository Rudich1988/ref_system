from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework.exceptions import ValidationError, NotFound
from typing_extensions import Optional
from django.db.models import Prefetch, Subquery, OuterRef, F

from utils.repository import AbstractRepository
from apps.users.models import CustomUser
from apps.invite_codes.models import InviteCode
from apps.invite_codes.serializers import (
    InviteCodeActivationSerializer,
    InviteCodeSerializer
)
from apps.users.serializers import (
    UserSerializer,
    UserModelSerializer,
    CustomUserSerializer
)


class UserRepository(AbstractRepository):
    def create(
            self,
            data: UserModelSerializer
    ) -> UserModelSerializer:
        try:
            data.is_valid(raise_exception=True)
            data = data.validated_data
            user = CustomUser.objects.create(
                **data
            )
            return UserModelSerializer(user)
        except ValidationError as e:
            raise e

    def get(
            self,
            data: UserSerializer
    ) -> Optional[UserModelSerializer]:
        try:
            data.is_valid(raise_exception=True)
            validated_data = data.validated_data
            user = CustomUser.objects.filter(
                **validated_data
            ).first()
            if not user:
                return None
            return UserModelSerializer(
                **validated_data
            )
        except ValidationError as e:
            raise e

    def get_profile(
            self,
            user_id
    ) -> CustomUserSerializer:
        try:
            user_data = CustomUser.objects.filter(id=user_id).annotate(
                referred_users_phone_numbers=ArrayAgg(
                    'invite_code__used_by__phone_number',
                    distinct=True
                )
            ).values(
                'id',
                'phone_number',
                'invite_code__code',
                'activated_invite_code__code',
                'referred_users_phone_numbers'
            ).first()
            referred_users = user_data[
                'referred_users_phone_numbers'
            ] \
                if user_data[
                       'referred_users_phone_numbers'
                   ][0] is not None else []
            data = {
                'id': user_data['id'],
                'phone_number': user_data['phone_number'],
                'invite_code': user_data[
                    'invite_code__code'
                ],
                'activated_invite_code': user_data[
                    'activated_invite_code__code'
                ],
                'referred_users_phone_numbers': referred_users
            }
            user_data = CustomUserSerializer(
                data=data
            )
            return user_data
        except CustomUser.DoesNotExist:
            raise NotFound(
                detail='user not found'
            )

    def active_invite_code(
            self,
            user_id: int,
            invite_code: InviteCodeActivationSerializer
    ) -> InviteCodeSerializer:
        try:
            invite_code.is_valid(
                raise_exception=True
            )
            code = InviteCode.objects.get(
                code=invite_code.validated_data['code']
            )
            user = CustomUser.objects.select_related(
                'invite_code'
            ).get(
                id=user_id
            )
            if user.activated_invite_code:
                raise ValidationError(
                    'User already has an activated invite code.'
                )
            if user.invite_code.id == code.id:
                raise ValidationError(
                    'invite_code not correct.'
                )

            user.activated_invite_code = code
            user.save()
            return InviteCodeSerializer(
                instance=code
            )
        except InviteCode.DoesNotExist:
            raise NotFound(
                detail='invite code not found'
            )
        except CustomUser.DoesNotExist:
            raise NotFound(
                detail='user not found'
            )
        except ValidationError as e:
            raise e
