# Generated by Django 3.2.3 on 2021-07-05 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patients', '0001_initial'),
        ('requesters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Последняя дата обновления')),
                ('daily_num', models.PositiveIntegerField(db_index=True, null=True, verbose_name='Порядковый номер за день')),
                ('total_num', models.PositiveIntegerField(null=True, unique=True, verbose_name='Порядковый номер')),
                ('reason', models.SmallIntegerField(choices=[(1, 'Беременность'), (2, 'Госпитализация'), (3, 'Контакт'), (4, 'Медицинский работник'), (5, 'Новорожденный'), (6, 'Острый бронхит'), (7, 'Обследование'), (8, 'Пневмония'), (9, 'Прибывшие'), (10, 'COVID-19'), (11, 'Хронический фарингит'), (12, 'Другое')], db_index=True, verbose_name='Цель исследования')),
                ('collect_date', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата поступления')),
                ('result_date', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата выдачи ответа')),
                ('analys_taken_date', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата взятия образца')),
                ('analys_taken_by', models.CharField(blank=True, db_index=True, default='', max_length=256, verbose_name='Лицо взявшее образец')),
                ('analys_transport_date', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата транспортировки образца')),
                ('analys_transport_by', models.CharField(blank=True, db_index=True, default='', max_length=256, verbose_name='Лицо транспортировавшее образец')),
                ('analys_transport_temp', models.SmallIntegerField(blank=True, db_index=True, null=True, verbose_name='Температура транспортировки образца')),
                ('result', models.SmallIntegerField(choices=[(0, 'Не готов'), (1, 'Положительный'), (-1, 'Отрицательный')], db_index=True, null=True, verbose_name='Результат')),
                ('note', models.TextField(blank=True, default='', verbose_name='Примечание')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient', verbose_name='Пациент')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requesters.requester', verbose_name='Направившая медицинская организация')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('total_num'), descending=True, nulls_last=False)],
            },
        ),
    ]
