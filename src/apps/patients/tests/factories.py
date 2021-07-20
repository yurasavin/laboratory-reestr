import random

import factory

from factory import Faker, Sequence
from factory.django import DjangoModelFactory

from apps.patients.models import Patient, PatientGenders

factory.Faker._DEFAULT_LOCALE = 'ru_RU'


class PatientFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    middle_name = Faker('middle_name')
    gender = Faker('random_element', elements=[ch[0] for ch in PatientGenders.choices])
    birthday = Faker('date')
    id_doc_type = 'паспорт'
    id_doc_series = Faker('random_number', digits=4)
    id_doc_num = Faker('random_number', digits=6)
    insurance_number = Faker('msisdn')
    insurance_company_id = Sequence(lambda n: n)
    self_phone = Faker('phone_number')
    work_phone = Faker('phone_number')
    reg_address = Faker('street_address')
    fact_address = Faker('street_address')
    work_address = Faker('street_address')
    work_place = Faker('company')
    work_post = Faker('job')

    class Meta:
        model = Patient
