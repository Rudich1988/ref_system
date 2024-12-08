from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.authentication.errors import PhoneAuthNotFoundError
from apps.authentication.models import PhoneAuth
from apps.authentication.services import AuthenticationService
from apps.authentication.serializers import (
    PhoneNumberSerializer,
    PhoneCodeSerializer
)
from apps.authentication.decorators import (
    phone_number_schema,
    verify_phone_number_schema
)


class PhoneAuthView(CreateAPIView):
    queryset = PhoneAuth.objects.all()
    serializer_class = PhoneNumberSerializer
    permission_classes = (AllowAny,)

    @phone_number_schema()
    def post(self, request, *args, **kwargs):
        try:
            serializer = PhoneNumberSerializer(
                data=request.data
            )
            serializer.is_valid(
                raise_exception=True
            )
            auth_code = AuthenticationService(
            ).get_verify_code(phone_data=serializer)
            return Response(
                data=auth_code.validated_data,
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {"detail": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyPhoneNumber(CreateAPIView):

    @verify_phone_number_schema()
    def post(self, request, *args, **kwargs):
        try:
            serializer = PhoneCodeSerializer(data=request.data)
            jwt_tokens = AuthenticationService().get_tokens(
                serializer
            )
            jwt_tokens.is_valid()
            return Response(
                data=jwt_tokens.validated_data,
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {"detail": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PhoneAuthNotFoundError as e:
            return Response(
                {"detail":str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
