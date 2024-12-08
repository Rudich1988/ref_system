from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView

schema_view = get_schema_view(
   openapi.Info(
      title="Referral System API",
      default_version='v1',
      description="API documentation for the referral system",
      contact=openapi.Contact(email="rudichdev@gmail.com"),
   ),
   authentication_classes=[JWTAuthentication],
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),

    path(
        'auth/',
        include(
            'apps.authentication.urls',
            namespace='authentication'
        )
    ),
    path(
        'users/',
        include(
            'apps.users.urls',
            namespace='users'
        ),
    ),
    path(
        'refresh_token/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
