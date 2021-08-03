import django_filters

from django.contrib.postgres.search import SearchVector
from django.db.models import Count, Q

from apps.researches.models import Research, ResearchResult


class BaseResearchFilter(django_filters.FilterSet):
    class Meta:
        model = Research
        fields = (
            'id', 'patient__first_name', 'patient__last_name',
            'patient__middle_name',
        )


def researches_search(*, qs, searches):
    searches_map = {
        'search_num': lambda qs, val: qs.filter(
            Q(daily_num=val) | Q(total_num=val)),

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
        for value in search_value.split():
            qs = search_func(qs, value)

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


def researches_stats():
    researches_stats = (
        Research.objects
        .exclude(result_date=None)
        .values('result_date__month', 'result_date__year')
        .annotate(
            positive_count=Count('id', filter=Q(result=ResearchResult.POSITIVE)),  # noqa: #501
            negative_count=Count('id', filter=Q(result=ResearchResult.NEGATIVE)),  # noqa: #501
        )
        .order_by('result_date__year', 'result_date__month')
    )
    months_map = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октяьрь',
        11: 'Ноябрь',
        12: 'Декабрь',
    }
    labels = []
    positive_dataset = {
        'label': 'Положительных',
        'backgroundColor': 'rgba(161, 29, 53, 0.7)',
        'data': [],
    }
    negative_dataset = {
        'label': 'Отрицательных',
        'backgroundColor': 'rgba(119, 191, 126, 0.7)',
        'data': [],
    }
    for stat in researches_stats:
        labels.append(' '.join([
            months_map[stat['result_date__month']],
            str(stat['result_date__year']),
        ]))
        positive_dataset['data'].append(stat['positive_count'])
        negative_dataset['data'].append(stat['negative_count'])

    return {'labels': labels, 'datasets': [positive_dataset, negative_dataset]}
