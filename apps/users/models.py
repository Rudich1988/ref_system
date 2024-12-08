from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.invite_codes.models import InviteCode


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        unique=True,
        max_length=15
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    activated_invite_code = models.ForeignKey(
        to=InviteCode,
        related_name='used_by',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    invite_code = models.OneToOneField(
        to=InviteCode,
        related_name='owner',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=['activated_invite_code'],
                name='customuser_act_invite_code_idx'
            ),
            models.Index(
                fields=['invite_code'],
                name='customuser_invite_code_idx'
            ),
            models.Index(
                fields=['phone_number'],
                name='customuser_phone_number_idx'
            )
        ]

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.phone_number
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number

    def __repr__(self):
        return (
            f'id: {self.pk}, '
            f'phone_number: {self.phone_number}'
        )
