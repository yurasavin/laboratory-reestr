# Generated by Django 3.2.3 on 2021-08-03 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researches', '0005_alter_research_options'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='research',
            name='daily_num_and_date',
        ),
        migrations.AlterField(
            model_name='research',
            name='analys_taken_date',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='Дата взятия образца'),
        ),
        migrations.AlterField(
            model_name='research',
            name='analys_transport_date',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='Дата транспортировки образца'),
        ),
        migrations.AlterField(
            model_name='research',
            name='collect_date',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='Дата поступления'),
        ),
        migrations.AlterField(
            model_name='research',
            name='result_date',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='Дата выдачи ответа'),
        ),
        migrations.AddConstraint(
            model_name='research',
            constraint=models.UniqueConstraint(fields=('daily_num', 'collect_date'), name='daily_num_and_date'),
        ),
    ]
