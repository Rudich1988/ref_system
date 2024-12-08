from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

def active_invite_code_schema():
    return swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='A1B2C3',
                    description="6-digit alphanumeric code that activates the invite"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                'Code successfully activated',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Activation status"
                        ),
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Activation message"
                        ),
                    }
                )
            ),
            400: openapi.Response('Bad Request'),
            404: openapi.Response('Not Found'),
            500: openapi.Response('Internal Server Error'),
        },
        security=[{'BearerAuth': []}]
    )
