from django.urls import path

from apps.users.views import UserProfileView, UserActiveCodeView

app_name = 'authentication'

urlpatterns = [
    path(
        '<int:id>/profile/',
        UserProfileView.as_view(),
        name='get_profile'
    ),
    path(
        '<int:id>/active_code/',
        UserActiveCodeView.as_view(),
        name='activate_code'
    )
]
