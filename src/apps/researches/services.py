import io

from babel.dates import format_date
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from openpyxl import load_workbook

from apps.patients.models import Patient
from apps.requesters.models import Requester
from apps.researches.models import Research


def research_create(*, research_data, user):
    patient_data = research_data.pop('patient')
    requester_data = research_data.pop('requester')

    patient = Patient.objects.create(**patient_data, created_by=user)
    requester = Requester.objects.create(**requester_data, created_by=user)

    researches = Research.objects.select_for_update()
    with transaction.atomic():
        today = timezone.make_naive(timezone.now()).date()
        total_num = researches.count() + 1
        daily_num = researches.filter(
            created_at__date=today).count() + 1

        research = Research.objects.create(
            total_num=total_num, daily_num=daily_num,
            patient=patient, requester=requester, **research_data,
            created_by=user)

    return research


def research_patch(*, research_data, user):
    patient_data = research_data.pop('patient')
    patient_id = patient_data.pop('id')
    Patient.objects.filter(
        id=patient_id).update(**patient_data, updated_by=user)

    requester_data = research_data.pop('requester')
    requester_id = requester_data.pop('id')
    Requester.objects.filter(
        id=requester_id).update(**requester_data, updated_by=user)

    research_id = research_data.pop('id')
    research = Research.objects.filter(id=research_id)
    research.update(**research_data, updated_by=user)

    return research.get()


def research_remove(*, research_id, user):
    Research.objects.filter(id=research_id).update(
        deleted=True, updated_by=user)


def research_export_to_xlsx(*, research_id):
    research = Research.objects.get(id=research_id)

    template_path = settings.BASE_DIR / 'src' / 'apps' / 'researches' / 'templates' / 'result_form.xlsx'  # noqa: #501
    wb = load_workbook(template_path)
    ws = wb.active

    # дата результата
    if research.result_date:
        value = research.result_date.astimezone()
        value = format_date(value, '«dd» MMMM Y г.', locale='ru_RU')
        ws['A3'].value = ws['C24'].value = value

    # номер анализа
    ws['B4'].value = research.total_num

    # ФИО
    if research.patient:
        ws['E3'].value = f'{research.patient.last_name} {research.patient.first_name} {research.patient.middle_name}'  # noqa:E501

    # направлен из
    ws['G5'].value = research.requester.name

    # диагноз
    ws['F7'].value = research.get_reason_display()

    # дата взятия
    if research.collect_date:
        value = research.collect_date.astimezone().strftime('%d.%m.%Y') + ' г.'
        ws['H9'].value = value

    # результат
    ws['E13'].value = research.get_result_display().upper()

    buffer = io.BytesIO()
    wb.save(buffer)
    wb.close()
    buffer.seek(0)
    return buffer
