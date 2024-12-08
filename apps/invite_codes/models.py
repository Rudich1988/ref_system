from django.db import models


class InviteCode(models.Model):
    code = models.CharField(
        max_length=6,
        unique=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=['code'],
                name='invite_code_code_idx'
            ),
        ]

    def __str__(self):
        return (
            f"Invite Code: {self.code}"
        )
