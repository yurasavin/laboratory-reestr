# Generated by Django 3.2.3 on 2021-08-02 19:58

from django.db import migrations

requesters_names = [
    'МБУЗ ЦГБ г.ДОНЕЦК РО',
    'ГБУ РО "КВД"',
    'ГБУ РО "КВД" ПЛАТНЫЕ УСЛУГИ',
    'МБУЗ ЦРБ АКСАЙСКОГО Р-НА',
    'МБУЗ ЦРБ Куйбышевского р-на',
    'Новочеркасский ф-л ГБУ РО "КВД"',
    'МБУЗ ЦРБ М-Курганского р-на',
    'Волгодонский ф-л ГБУ РО "КВД"',
    'МБУЗ ЦРБ Неклиновского р-на',
    'Таганрогский ф-л ГБУ РО "КВД"',
    'МБУЗ ЦРБ Кагальницкого р-на',
    'Новошахтинский ф-л ГБУ РО "КВД"',
    'К-Шахтинский ф-л ГБУ РО "КВД"',
    'Шолоховский ф-ал ГБУ РО "КВД"',
    'ГБУ РО "Наркологический диспансер"',
    'Азовский ф-л ГБУ РО "НД"',
    'Гуковский ф-л ГБУ РО "НД"',
    'МБУЗ ГБ №3 г.ТАГАНРОГ',
    'МБУЗ ГБ №7 г.ТАГАНРОГ',
    'МБУЗ ГБ №2 г.ШАХТЫ',
    'МБУЗ ГБСМП г.ТАГАНРОГ',
    'МБУЗ ГБСМП г.ШАХТЫ',
    'МБУЗ ГП №1 г.ТАГАНРОГ',
    'МБУЗ ГП №1 г.ШАХТЫ',
    'МБУЗ ГП №2 г.ТАГАНРОГ',
    'МБУЗ ГП №2 г.ШАХТЫ',
    'МБУЗ ДГБ г.ТАГАНРОГ',
    'МБУЗ ГП №5 г.ШАХТЫ',
    'МБУЗ ДГП №1 г.ТАГАНРОГ',
    'МБУЗ ГП г.ШАХТЫ',
    'МБУЗ ДГП №2 г.ТАГАНРОГ',
    'МБУЗ ДГБ г.ШАХТЫ',
    'МБУЗ КДЦ г.ТАГАНРОГ',
    'МБУЗ РД г.ТАГАНРОГ',
    'ООО "Городской центр экспертиз"',
    'ООО МНПО "ЗДОРОВЬЕ НАЦИИ"',
    'ООО "ТАМИ"',
    'ООО "Альянс-2000"',
    'ГБУ РО "СПК"',
    'МСЧ ПАО "ТАНТК им.Г.М.Бериева"',
    'ГБУ РО "РОКБ"',
    'МБУЗ "ЦГБ" г.Азов',
    'ГБУЗ "Кущевская ЦРБ" МЗ КК',
    'Азовский ф-ал ГБУ РО "ПНД"',
    'АО "Ростовоблфармация"',
    'Аксайский ф-ал ГБУ РО "ПНД"',
    'Ф-ал ООО "Капитал МС" в РО ГБУ РО "ПНД"',
    'ГБУ РО "ЦПиБ со СПИД"',
    'ГБПОУ РО "РОУОР"',
    'ГКУ СО РО "РЦПД №10"',
    'МСЧ АО "ТАГМЕТ"',
    'ЧУЗ МСЧ "Красный котельщик"',
    'ГКУ СО РО "РЦПД №4"',
    'АО "ТКЭ"',
    'ГАУК РО "РГТК им.В.С.Былкова"',
    'МБУЗ "Стоматологическая пол-ка №5"',
    'ООО "Умка-Фэмили"',
    'ГОУ РО "Ростов.спец.школа-интернат №41"',
    'ГБУ РО "СШОР №5"',
]


def create_requesters(apps, schema_editor, *args, **kwargs):
    Requester = apps.get_model('requesters', 'Requester')
    Requester.objects.bulk_create(
        [Requester(name=name) for name in requesters_names],
    )


class Migration(migrations.Migration):

    dependencies = [
        ('requesters', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_requesters, migrations.RunPython.noop),
    ]
