from django.db import models

from apps.core.models import TimeStampedByUserModel


class PatientGenders(models.IntegerChoices):
    FEMALE = (0, 'Женский')
    MALE = (1, 'Мужской')


class Patient(TimeStampedByUserModel):
    first_name = models.CharField('Имя', max_length=128, db_index=True)
    last_name = models.CharField('Фамилия', max_length=128, db_index=True)
    middle_name = models.CharField(
        'Отчество',
        max_length=128,
        db_index=True,
        default='',
    )
    gender = models.PositiveSmallIntegerField(
        'Пол',
        choices=PatientGenders.choices,
    )
    birthday = models.DateField('Дата рождения')
    id_doc_type = models.CharField(
        'Документ подтверждающий личность',
        max_length=32,
        default='',
        blank=True,
    )
    id_doc_series = models.CharField(
        'Серия документа',
        max_length=32,
        default='',
        blank=True,
    )
    id_doc_num = models.CharField(
        'Номер документа',
        max_length=32,
        default='',
        blank=True,
    )
    insurance_number = models.CharField(
        'Номер страхового полиса',
        max_length=64,
        default='',
        blank=True,
    )
    insurance_company_id = models.CharField(
        'Реестровый номер страховой компании',
        max_length=128,
        default='',
        blank=True,
    )
    self_phone = models.CharField(
        'Контактный номер телефона',
        max_length=64,
        default='',
        blank=True,
    )
    reg_address = models.CharField(
        'Адрес регистрации',
        max_length=512,
        default='',
        blank=True,
    )
    fact_address = models.CharField(
        'Адрес фактический',
        max_length=512,
        default='',
        blank=True,
    )
    work_address = models.CharField(
        'Адрес работы/учебы',
        max_length=512,
        default='',
        blank=True,
    )
    work_place = models.CharField(
        'Место работы/учебы',
        max_length=512,
        default='',
        blank=True,
    )
    work_post = models.CharField(
        'Должность',
        max_length=128,
        default='',
        blank=True,
    )

    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name']

    def __str__(self):
        return f'{self.id}'
