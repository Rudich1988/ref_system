from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.errors import PhoneAuthNotFoundError
from apps.users.models import CustomUser
from apps.users.serializers import UserModelSerializer
from utils.repository import AbstractRepository
from apps.authentication.models import PhoneAuth
from apps.authentication.serializers import PhoneAuthSerializer, TokensSerializer


class AuthenticationRepository(AbstractRepository):
    def create(
            self,
            data: PhoneAuthSerializer
    ) -> PhoneAuthSerializer:
        try:
            data = data.validated_data
            phone_auth_instance = PhoneAuth.objects.create(
                **data
            )
            return PhoneAuthSerializer(phone_auth_instance)
        except Exception as e:
            raise Exception(
                f"Error creating authentication info: {str(e)}"
            )

    def get(
            self,
            data: PhoneAuthSerializer
    ) -> PhoneAuthSerializer:
        try:
            phone_number = data.validated_data.get(
                "phone_number"
            )
            code = data.validated_data.get("code")

            phone_auth_instance = PhoneAuth.objects.filter(
                phone_number=phone_number,
                code=code,
                expires_at__gt=timezone.now()
            ).first()

            if not phone_auth_instance:
                raise PhoneAuthNotFoundError(
                    "Invalid or expired code."
                )
            return PhoneAuthSerializer(
                phone_auth_instance
            )
        except PhoneAuthNotFoundError as e:
            raise e
        except Exception as e:
            raise Exception(
                f"Error retrieving PhoneAuth: {str(e)}"
            )

    def create_tokens(
            self,
            user_data: UserModelSerializer
    ) -> TokensSerializer:
        user = CustomUser.objects.filter(
            **user_data.data
        ).first()
        refresh = RefreshToken.for_user(user)
        return TokensSerializer(
            data={
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token)
        }
        )
