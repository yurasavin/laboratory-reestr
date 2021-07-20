import django_filters

from django.contrib.postgres.search import SearchVector

from apps.researches.models import Research


class BaseResearchFilter(django_filters.FilterSet):
    class Meta:
        model = Research
        fields = (
            'id', 'patient__first_name', 'patient__last_name',
            'patient__middle_name'
        )


def researches_search(*, qs, searches):
    searches_map = {
        'search_num': lambda qs, val: qs.annotate(
            search_num=SearchVector('daily_num', 'total_num'),
        ).filter(search_num__contains=val),

        'search_patient': lambda qs, val: qs.annotate(
            search_patient=SearchVector(
                'patient__first_name',
                'patient__last_name',
                'patient__middle_name',
            )).filter(search_patient__contains=val),

        'search_requester': lambda qs, val: qs.annotate(
            search_requester=SearchVector(
                'requester__name',
                'requester__oms_id',
            )).filter(search_requester__contains=val),
    }

    for search_name in searches:
        search_func = searches_map[search_name]
        search_value = searches[search_name]
        qs = search_func(qs, search_value)

    return qs


def researches_list(*, filters_and_searches=None):
    filters_and_searches = filters_and_searches or {}
    filters = {}
    searches = {}

    for key in filters_and_searches:
        if key.startswith('search_'):
            searches[key] = filters_and_searches[key]
        else:
            filters[key] = filters_and_searches[key]

    qs = Research.objects.filter(deleted=False).select_related(
        'patient', 'requester')
    qs = BaseResearchFilter(filters, qs).qs
    qs = researches_search(qs=qs, searches=searches)

    return qs
