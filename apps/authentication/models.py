from datetime import timedelta

from django.db import models
from django.utils import timezone


class PhoneAuth(models.Model):
    phone_number = models.CharField(
        max_length=12,
    )
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(
                fields=['phone_number', 'code'],
                name='phoneauth_phone_code_idx'
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.expires_at:
            if self.created_at is None:
                self.created_at = timezone.now()
            self.expires_at = self.created_at +\
                              timedelta(minutes=5)

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Phone: {self.phone_number}, "
            f"Code: {self.code}, "
            f"Expires at: {self.expires_at}"
        )
