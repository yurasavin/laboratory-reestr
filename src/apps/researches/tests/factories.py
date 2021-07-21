import factory

from factory import Faker, Sequence, SubFactory
from factory.django import DjangoModelFactory

from apps.patients.tests.factories import PatientFactory
from apps.requesters.tests.factories import RequesterFactory
from apps.researches.models import Research, ResearchReasons, ResearchResult

factory.Faker._DEFAULT_LOCALE = 'ru_RU'


class ResearchFactory(DjangoModelFactory):
    patient = SubFactory(PatientFactory)
    daily_num = Sequence(lambda n: n)
    total_num = Sequence(lambda n: n)
    requester = SubFactory(RequesterFactory)
    reason = Faker('random_element', elements=[ch[0] for ch in ResearchReasons.choices])
    collect_date = Faker('date_time_between', start_date='-1y', end_date='now',)
    result_date = Faker('date_time_between', start_date='-1y', end_date='now',)
    analys_taken_date = Faker('date_time_between', start_date='-1y', end_date='now',)
    analys_taken_by = Faker('name')
    analys_transport_date = Faker('date_time_between', start_date='-1y', end_date='now',)
    analys_transport_by = Faker('name')
    analys_transport_temp = Faker('random_int', min=-20, max=20)
    result = Faker('random_element', elements=[ch[0] for ch in ResearchResult.choices])
    note = Faker('catch_phrase')

    class Meta:
        model = Research
