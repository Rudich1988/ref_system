from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status

from apps.users.repository import UserRepository
from refer_system.permissions import IsOwnerOrAdmin
from .decorators import active_invite_code_schema
from .serializers import CustomUserSerializer
from .service import UserService
from ..invite_codes.serializers import InviteCodeActivationSerializer


class UserProfileView(generics.GenericAPIView):
    repository = UserRepository()
    serializer_class = CustomUserSerializer
    permission_classes = (
        #IsAuthenticated,
        #IsOwnerOrAdmin
    )

    def get(
            self,
            request,
            id: int,
            *args,
            **kwargs
    ):
        try:
            user_data = UserService().get_profile(
                user_id=id
            )
            user_data.is_valid(raise_exception=True)
            return Response(
                user_data.validated_data,
                status=status.HTTP_200_OK
            )
        except NotFound as e:
            return Response(
                {"detal": str(e)},
                status=status.HTTP_404_NOT_FOUND
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


class UserActiveCodeView(generics.GenericAPIView):
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrAdmin
    )

    @active_invite_code_schema()
    def post(
            self,
            request,
            id,
            *args,
            **kwargs
    ):
        try:
            invite_code = InviteCodeActivationSerializer(
                data={'code': request.data['code']}
            )
            code = UserService().active_invite_code(
                invite_code=invite_code,
                user_id=id
            )
            return Response(
                {'activated_invite_code': code.data.get('code')}
            )
        except NotFound as e:
            return Response(
                {"detal": str(e)},
                status=status.HTTP_404_NOT_FOUND
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
