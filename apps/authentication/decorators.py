from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def phone_number_schema():
    return swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='+79123456789',
                    description="Phone number with a valid prefix"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                'Success',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(
                            type=openapi.TYPE_STRING
                        )
                    }
                )
            )
        },
    )


def verify_phone_number_schema():
    return swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='+79123456789',
                    description="Phone number with a valid prefix"
                ),
                'code': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='1234',
                    description="Verification code sent to the phone number"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                'Success',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh_token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="JWT refresh token"
                        ),
                        'access_token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="JWT access token"
                        ),
                    }
                )
            ),
            400: openapi.Response('Bad Request'),
            404: openapi.Response('Not Found'),
            500: openapi.Response('Internal Server Error'),
        },
    )
