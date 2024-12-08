from apps.authentication.repository import AuthenticationRepository
from apps.invite_codes.service import InviteCodeService
from apps.users.repository import UserRepository
from apps.users.serializers import UserModelSerializer, UserSerializer
from services.verify_services.sms_verify_service import SmsVerifyService
from apps.authentication.serializers import (
    PhoneAuthSerializer,
    PhoneNumberSerializer,
    PhoneCodeSerializer,
    TokensSerializer,
    VerifyCodeSerializer
)


class AuthenticationService:
    def get_verify_code(
            self,
            phone_data: PhoneNumberSerializer
    ) -> VerifyCodeSerializer:
        phone_number = self.prepare_phone_number(
            phone_number=phone_data.validated_data[
                'phone_number'
            ]
        )
        auth_code = SmsVerifyService().create_code()
        auth_code.is_valid(raise_exception=True)
        phone_auth_serializer = PhoneAuthSerializer(
            data={
                'phone_number': phone_number,
                'code': auth_code.data.get('code')
            }
        )
        phone_auth_serializer.is_valid(
            raise_exception=True
        )
        AuthenticationRepository().create(
            phone_auth_serializer
        )
        return auth_code

    def get_tokens(
            self,
            data: PhoneCodeSerializer
    ) -> TokensSerializer:
        data.is_valid(raise_exception=True)
        phone_number = self.prepare_phone_number(
            phone_number=data.validated_data[
                'phone_number'
            ]
        )
        auth_code = data.validated_data[
            'code'
        ]
        phone_auth_serializer = PhoneAuthSerializer(
            data={
                'phone_number': phone_number,
                'code': auth_code
            }
        )
        phone_auth_serializer.is_valid(
            raise_exception=True
        )
        phone_auth = AuthenticationRepository().get(
            phone_auth_serializer
        )

        user_data = UserSerializer(
            data={
                'phone_number': phone_auth.data[
                    'phone_number'
                ]
            }
        )
        user = UserRepository().get(user_data)
        if not user:
            invite_code = InviteCodeService().create()
            invite_code = invite_code.data

            user_data = UserModelSerializer(
                data={
                    'invite_code': invite_code['id'],
                    'phone_number': phone_auth.data[
                        'phone_number'
                    ]
                }
            )
            user = UserRepository().create(
                user_data
            )
        jwt_tokens = self.create_tokens(
            user
        )
        return jwt_tokens

    def create_tokens(
            self,
            user: UserModelSerializer
    ) -> TokensSerializer:
        return AuthenticationRepository().create_tokens(
            user_data=user
        )

    def prepare_phone_number(
            self,
            phone_number: str
    ) -> str:
        if phone_number[0] == '8':
            phone_number = '+7' + phone_number[1:]
        return phone_number
