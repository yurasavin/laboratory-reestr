from apps.limits.models import LimitMoney, Subdivision

DB_ZERO_DECIMAL_VALUE = Value(0, output_field=models.DecimalField())


def get_totals_by_subdivisions(self: 'Source'):
        subdivisions = self.subdivision_set \
            .annotate(
                contracts_money=Coalesce(
                    Subquery(
                        ContractPrice.objects
                            .filter(subdivision=OuterRef('pk'))
                            .values('subdivision')
                            .annotate(total_money=Sum('money'))
                            .values('total_money')
                    ),
                    DB_ZERO_DECIMAL_VALUE,
                ),
                contracts_delta=Coalesce(
                    Subquery(
                        ContractPriceChange.objects
                            .filter(price__subdivision=OuterRef('pk'))
                            .values('price__subdivision')
                            .annotate(total_delta=Sum('delta'))
                            .values('total_delta')
                    ),
                    DB_ZERO_DECIMAL_VALUE,
                ),
                used=F('contracts_money') + F('contracts_delta'),
                in_use=Coalesce(
                    Subquery(
                        StartPrice.objects
                            .filter(
                                subdivision=OuterRef('pk'),
                                tender__status='in_work',
                            )
                            .values('subdivision')
                            .annotate(tenders_money=Sum('money'))
                            .distinct()
                            .values('tenders_money'),
                    ),
                    DB_ZERO_DECIMAL_VALUE,
                ),
            )

        return {subdiv['num']: subdiv for subdiv in subdivisions.values()}


def get_under_100_contracts_44_fz(self: 'Limit'):  # noqa: WPS210
        """
        Возвращает кверисет LimitMoney, по которым
        заключены контракты до 600 т.р. по 44-ФЗ
        """
        objects = LimitMoney.objects.filter(
            industry_code__limit_article__source__limit=self,
            contractprice__contract__ticket__tender_type__law=44,
            contractprice__contract__ticket__tender_type__name='ЕП до 600',
        )
        total = objects.aggregate(total=Sum('contractprice__money'))['total']
        total = total if total else 0

        delta = objects.aggregate(
            delta=Sum('contractprice__contractpricechange__delta'),
        )['delta']
        delta = delta if delta else 0

        total_with_delta = total + delta

        total_plan = LimitMoney.objects.filter(
            industry_code__limit_article__source__limit=self,
            industry_code__limit_article__source__num__in=[4, 5, 7],
        ).aggregate(m=Sum('money'))['m']
        percent = Decimal('0.10') if self.year >= 2020 else Decimal('0.05')
        total_plan = total_plan * percent if total_plan else 0
        if total_plan < 2_000_000:
            total_plan = 2_000_000

        total_balance = total_plan - total_with_delta

        objects = objects.annotate(
            used=Sum('contractprice__money'),
            delta=Sum('contractprice__contractpricechange__delta'),
        ).order_by(
            'industry_code__limit_article__source__num',
            'industry_code__limit_article__num',
            'industry_code__num',
            'sybsidy_code',
        ).prefetch_related(
            'industry_code__limit_article__source',
        )
        return [[objects, total, total_with_delta, total_plan, total_balance]]


def get_limit_data(self: 'Limit'):  # noqa: WPS210
        """
        Возвращает сводную информацию о лимитах
        """
        limit_moneys = LimitMoney.objects \
            .filter(industry_code__limit_article__source__limit=self) \
            .select_related('industry_code__limit_article__source') \
            .annotate(
                contracts_money=Coalesce(
                    Subquery(
                        ContractPrice.objects
                            .filter(limit=OuterRef('pk'))
                            .values('limit')
                            .annotate(total_money=Sum('money'))
                            .values('total_money'),
                    ),
                    DB_ZERO_DECIMAL_VALUE,
                ),
                contracts_delta=Coalesce(
                    Subquery(
                        ContractPriceChange.objects
                            .filter(price__limit=OuterRef('pk'))
                            .values('price__limit')
                            .annotate(total_delta=Sum('delta'))
                            .values('total_delta'),
                    ),
                    DB_ZERO_DECIMAL_VALUE,
                ),
                used_with_delta=F('contracts_money') + F('contracts_delta'),
                tenders_money=Coalesce(
                    Sum(
                        'startprice__money',
                        filter=Q(startprice__tender__status='in_work'),
                    ),
                    DB_ZERO_DECIMAL_VALUE,
                ),
            ) \
            .order_by(
                'industry_code__limit_article__source__num',
                'industry_code__limit_article__num',
                'industry_code__num',
                'sybsidy_code',
            )

        limit_info = {}
        for limit_money in limit_moneys:
            source = limit_money.industry_code.limit_article.source
            article = limit_money.industry_code.limit_article
            industry_code = limit_money.industry_code

            source_data = limit_info.get(
                source.id,
                {
                    'id': source.id,
                    'name': source.name,
                    'num': source.num,
                    'total': Decimal('0.00'),
                    'in_use': Decimal('0.00'),
                    'used': Decimal('0.00'),
                    'articles': {},
                    'subdivisions': {},
                },
            )

            if not source_data['subdivisions']:
                source_data['subdivisions'] = source.get_totals_by_subdivisions()  # noqa: E501

            article_data = source_data['articles'].get(
                article.id,
                {
                    'id': article.id,
                    'num': article.num,
                    'name': article.name,
                    'row_span': 1,
                    'total': Decimal('0.00'),
                    'in_use': Decimal('0.00'),
                    'used': Decimal('0.00'),
                    'industry_codes': {},
                },
            )

            article_data['industry_codes'][limit_money.id] = {
                'id': limit_money.id,
                'money': limit_money.money,
                'industry_code__name': industry_code.name,
                'industry_code__num': industry_code.num,
                'sybsidy_code': limit_money.sybsidy_code,
                'in_use': limit_money.tenders_money,
                'used': limit_money.used_with_delta,
            }

            article_data['row_span'] += 1
            article_data['total'] += limit_money.money
            article_data['in_use'] += limit_money.tenders_money
            article_data['used'] += limit_money.used_with_delta

            source_data['total'] += limit_money.money
            source_data['in_use'] += limit_money.tenders_money
            source_data['used'] += limit_money.used_with_delta

            source_data['articles'][article.id] = article_data
            limit_info[source.id] = source_data

        return limit_info
