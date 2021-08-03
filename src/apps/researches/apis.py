from django.http import FileResponse
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from apps.api.pagination import get_paginated_response
from apps.api.permissions import WriteEditDeletePermission
from apps.patients.models import Patient
from apps.requesters.models import Requester
from apps.researches.models import Research
from apps.researches.selectors import researches_list, researches_stats
from apps.researches.services import (research_create, research_export_to_xlsx,
                                      research_patch, research_remove)


class ResearchListView(viewsets.GenericViewSet):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class FilterSerializer(serializers.Serializer):
        search_num = serializers.CharField(required=False)
        search_patient = serializers.CharField(required=False)
        search_requester = serializers.CharField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class PatientSerializer(serializers.ModelSerializer):
            class Meta:
                model = Patient
                fields = [
                    'id',
                    'first_name',
                    'last_name',
                    'middle_name',
                    'gender',
                    'birthday',
                    'id_doc_type',
                    'id_doc_series',
                    'id_doc_num',
                    'insurance_number',
                    'insurance_company_id',
                    'self_phone',
                    'reg_address',
                    'fact_address',
                    'work_address',
                    'work_place',
                    'work_post',
                ]

        class RequesterSerializer(serializers.ModelSerializer):
            class Meta:
                model = Requester
                fields = ['id', 'name', 'oms_id']

        patient = PatientSerializer(required=True)
        requester = RequesterSerializer(required=True)

        reason_display = serializers.SerializerMethodField()
        result_display = serializers.SerializerMethodField()
        collect_date_display = serializers.SerializerMethodField()
        result_date_display = serializers.SerializerMethodField()
        analys_taken_date_display = serializers.SerializerMethodField()
        analys_transport_date_display = serializers.SerializerMethodField()

        class Meta:
            model = Research
            fields = [
                'id',
                'total_num',
                'daily_num',
                'patient',
                'requester',
                'reason',
                'reason_display',
                'collect_date',
                'collect_date_display',
                'result_date',
                'result_date_display',
                'analys_taken_date',
                'analys_taken_date_display',
                'analys_taken_by',
                'analys_transport_date',
                'analys_transport_date_display',
                'analys_transport_by',
                'analys_transport_temp',
                'result',
                'result_display',
                'note',
            ]

        def get_reason_display(self, research):
            return research.get_reason_display()

        def get_result_display(self, research):
            return research.get_result_display()

        def get_collect_date_display(self, research):
            date = research.collect_date
            return None if not date else date.astimezone().strftime('%d.%m.%Y %H:%M')  # noqa: #501

        def get_result_date_display(self, research):
            date = research.result_date
            return None if not date else date.astimezone().strftime('%d.%m.%Y %H:%M')  # noqa: #501

        def get_analys_taken_date_display(self, research):
            date = research.analys_taken_date
            return None if not date else date.astimezone().strftime('%d.%m.%Y %H:%M')  # noqa: #501

        def get_analys_transport_date_display(self, research):
            date = research.analys_transport_date
            return None if not date else date.astimezone().strftime('%d.%m.%Y %H:%M')  # noqa: #501

    def list(self, request):
        filters_and_searches_serializer = self.FilterSerializer(
            data=request.query_params)
        filters_and_searches_serializer.is_valid(raise_exception=True)
        filters_and_searches = filters_and_searches_serializer.validated_data

        researches = researches_list(filters_and_searches=filters_and_searches)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=researches,
            request=request,
            view=self,
        )


class ResearchCreateView(viewsets.GenericViewSet):
    permission_classes = [WriteEditDeletePermission]

    class InputSerializer(serializers.ModelSerializer):
        class PatientSerializer(serializers.ModelSerializer):
            class Meta:
                model = Patient
                fields = [
                    'first_name',
                    'last_name',
                    'middle_name',
                    'gender',
                    'birthday',
                    'id_doc_type',
                    'id_doc_series',
                    'id_doc_num',
                    'insurance_number',
                    'insurance_company_id',
                    'self_phone',
                    'reg_address',
                    'fact_address',
                    'work_address',
                    'work_place',
                    'work_post',
                ]

        class RequesterSerializer(serializers.ModelSerializer):
            id = serializers.IntegerField()

            class Meta:
                model = Requester
                fields = ['id']

        patient = PatientSerializer(required=True)
        requester = RequesterSerializer(required=True)

        class Meta:
            model = Research
            fields = [
                'daily_num',
                'patient',
                'requester',
                'reason',
                'collect_date',
                'result_date',
                'analys_taken_date',
                'analys_taken_by',
                'analys_transport_date',
                'analys_transport_by',
                'analys_transport_temp',
                'result',
                'note',
            ]

    def create(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        research_create(
            research_data=input_serializer.validated_data, user=request.user)

        return Response(status=status.HTTP_201_CREATED)


class ResearchPatchView(viewsets.GenericViewSet):
    permission_classes = [WriteEditDeletePermission]

    class InputSerializer(serializers.ModelSerializer):
        class PatientSerializer(serializers.ModelSerializer):
            id = serializers.IntegerField()

            class Meta:
                model = Patient
                fields = [
                    'id',
                    'first_name',
                    'last_name',
                    'middle_name',
                    'gender',
                    'birthday',
                    'id_doc_type',
                    'id_doc_series',
                    'id_doc_num',
                    'insurance_number',
                    'insurance_company_id',
                    'self_phone',
                    'reg_address',
                    'fact_address',
                    'work_address',
                    'work_place',
                    'work_post',
                ]

        class RequesterSerializer(serializers.ModelSerializer):
            id = serializers.IntegerField()

            class Meta:
                model = Requester
                fields = ['id']

        id = serializers.IntegerField()
        patient = PatientSerializer(required=True)
        requester = RequesterSerializer(required=True)

        class Meta:
            model = Research
            fields = [
                'id',
                'daily_num',
                'patient',
                'requester',
                'reason',
                'collect_date',
                'result_date',
                'analys_taken_date',
                'analys_taken_by',
                'analys_transport_date',
                'analys_transport_by',
                'analys_transport_temp',
                'result',
                'note',
            ]

    class OutputSerializer(serializers.ModelSerializer):
        class PatientSerializer(serializers.ModelSerializer):
            class Meta:
                model = Patient
                fields = [
                    'id',
                    'first_name',
                    'last_name',
                    'middle_name',
                    'gender',
                    'birthday',
                    'id_doc_type',
                    'id_doc_series',
                    'id_doc_num',
                    'insurance_number',
                    'insurance_company_id',
                    'self_phone',
                    'reg_address',
                    'fact_address',
                    'work_address',
                    'work_place',
                    'work_post',
                ]

        class RequesterSerializer(serializers.ModelSerializer):
            class Meta:
                model = Requester
                fields = ['id', 'name', 'oms_id']

        patient = PatientSerializer(required=True)
        requester = RequesterSerializer(required=True)

        reason_display = serializers.SerializerMethodField()
        result_display = serializers.SerializerMethodField()
        collect_date_display = serializers.SerializerMethodField()
        result_date_display = serializers.SerializerMethodField()
        analys_taken_date_display = serializers.SerializerMethodField()
        analys_transport_date_display = serializers.SerializerMethodField()

        class Meta:
            model = Research
            fields = [
                'id',
                'total_num',
                'daily_num',
                'patient',
                'requester',
                'reason',
                'reason_display',
                'collect_date',
                'collect_date_display',
                'result_date',
                'result_date_display',
                'analys_taken_date',
                'analys_taken_date_display',
                'analys_taken_by',
                'analys_transport_date',
                'analys_transport_date_display',
                'analys_transport_by',
                'analys_transport_temp',
                'result',
                'result_display',
                'note',
            ]

        def get_reason_display(self, research):
            return research.get_reason_display()

        def get_result_display(self, research):
            return research.get_result_display()

        def get_collect_date_display(self, research):
            date = research.collect_date
            return None if not date else date.astimezone().strftime('%d.%m.%Y %H:%M')  # noqa: #501

        def get_result_date_display(self, research):
            date = research.result_date
            return None if not date else date.astimezone().strftime('%d.%m.%Y %H:%M')  # noqa: #501

        def get_analys_taken_date_display(self, research):
            date = research.analys_taken_date
            return None if not date else date.astimezone().strftime('%d.%m.%Y %H:%M')  # noqa: #501

        def get_analys_transport_date_display(self, research):
            date = research.analys_transport_date
            return None if not date else date.astimezone().strftime('%d.%m.%Y %H:%M')  # noqa: #501

    @action(methods=['post'], detail=False)
    def patch(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        research = research_patch(
            research_data=input_serializer.validated_data, user=request.user)
        output_data = self.OutputSerializer(instance=research).data

        return Response(output_data, status=status.HTTP_200_OK)


class ResearchRemoveView(viewsets.GenericViewSet):
    permission_classes = [WriteEditDeletePermission]

    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()

    @action(methods=['post'], detail=False)
    def remove(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        research_id = input_serializer.validated_data['id']
        research_remove(research_id=research_id, user=request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ResearchExportView(viewsets.GenericViewSet):
    class InputSerializer(serializers.Serializer):
        reagents = serializers.CharField()
        series = serializers.CharField()
        expiration_date = serializers.CharField()
        doctor = serializers.CharField()

    @action(methods=['post'], detail=True)
    def export(self, request, pk=None):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        response_bytes = research_export_to_xlsx(
            research_id=pk, **input_serializer.validated_data)

        return FileResponse(response_bytes, as_attachment=True)


class ResearchStatsView(viewsets.GenericViewSet):
    @action(methods=['get'], detail=False)
    def stats(self, request):
        response_data = researches_stats()
        return Response(response_data)
