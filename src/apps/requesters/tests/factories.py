import factory

from factory import Faker, Sequence
from factory.django import DjangoModelFactory

from apps.requesters.models import Requester

factory.Faker._DEFAULT_LOCALE = 'ru_RU'

class RequesterFactory(DjangoModelFactory):
    name = Faker('company')
    oms_id = Sequence(lambda n: n)

    class Meta:
        model = Requester
