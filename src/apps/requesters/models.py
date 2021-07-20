from django.db import models

from apps.core.models import TimeStampedByUserModel


class Requester(TimeStampedByUserModel):
    name = models.CharField('Наименование', max_length=256, db_index=True)
    oms_id = models.CharField(
        'Код МО в ОМС',
        max_length=32,
        default='',
        blank=True,
        db_index=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.id}'
