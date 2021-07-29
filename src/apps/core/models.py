from django.db import models

from apps.users.models import User


class TimeStampedByUserModel(models.Model):
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        'Последняя дата обновления',
        auto_now=True,
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
    )

    class Meta:
        abstract = True
