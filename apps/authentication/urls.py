from django.urls import path

from .views import PhoneAuthView, VerifyPhoneNumber

app_name = 'authentication'

urlpatterns = [
    path(
        '',
        PhoneAuthView.as_view(),
        name='create_code'
    ),
    path(
        'verify_phone_number/',
        VerifyPhoneNumber.as_view(),
        name='verify_phone_number'
    )
]
