from apps.requesters.models import Requester


def requesters_list():
    return Requester.objects.all()
