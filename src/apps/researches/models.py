from django.db import models

from apps.core.models import TimeStampedByUserModel
from apps.patients.models import Patient
from apps.requesters.models import Requester


class ResearchReasons(models.IntegerChoices):
    PREGNANCY = (1, 'Беременность')
    HOSPITALIZATION = (2, 'Госпитализация')
    CONTACT = (3, 'Контакт')
    MEDICAL_WORKER = (4, 'Медицинский работник')
    NEWBORN_BABY = (5, 'Новорожденный')
    ACUTE_BRONCHITIS = (6, 'Острый бронхит')
    SURVEY = (7, 'Обследование')
    PNEUMONIA = (8, 'Пневмония')
    ARRIVALS = (9, 'Прибывшие')
    COVID_19 = (10, 'COVID-19')
    CHRONIC_PHARYNGITIS = (11, 'Хронический фарингит')
    OTHER = (12, 'Другое')
    ORVI = (13, 'ОРВИ')


class ResearchResult(models.IntegerChoices):
    NOT_READY = 0, 'Не готов'
    POSITIVE = 1, 'Положительный'
    NEGATIVE = -1, 'Отрицательный'


class Research(TimeStampedByUserModel):
    daily_num = models.PositiveIntegerField(
        'Порядковый номер за день',
        null=True,
        db_index=True,
    )
    total_num = models.PositiveIntegerField(
        'Порядковый номер',
        null=True,
        unique=True,
    )
    patient = models.ForeignKey(
        Patient,
        verbose_name='Пациент',
        on_delete=models.CASCADE,
    )
    requester = models.ForeignKey(
        Requester,
        verbose_name='Направившая медицинская организация',
        on_delete=models.CASCADE,
    )
    reason = models.SmallIntegerField(
        'Цель исследования',
        choices=ResearchReasons.choices,
        db_index=True,
    )
    collect_date = models.DateField('Дата поступления', db_index=True)
    result_date = models.DateField(
        'Дата выдачи ответа',
        null=True,
        db_index=True,
        blank=True)
    analys_taken_date = models.DateField(
        'Дата взятия образца',
        null=True,
        db_index=True,
        blank=True)
    analys_taken_by = models.CharField(
        'Лицо взявшее образец',
        max_length=256,
        default='',
        db_index=True,
        blank=True,
    )
    analys_transport_date = models.DateField(
        'Дата транспортировки образца',
        null=True,
        db_index=True,
        blank=True,
    )
    analys_transport_by = models.CharField(
        'Лицо транспортировавшее образец',
        max_length=256,
        default='',
        db_index=True,
        blank=True,
    )
    analys_transport_temp = models.SmallIntegerField(
        'Температура транспортировки образца',
        null=True,
        db_index=True,
        blank=True,
    )
    result = models.SmallIntegerField(
        'Результат',
        null=True,
        db_index=True,
        choices=ResearchResult.choices,
    )
    note = models.TextField('Примечание', default='', blank=True)
    deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = [models.F('total_num').desc(nulls_last=False)]
        constraints = [
            models.UniqueConstraint(fields=['daily_num', 'collect_date'],
                                    name='daily_num_and_date'),
        ]

    def __str__(self):
        return f'{self.id}'
