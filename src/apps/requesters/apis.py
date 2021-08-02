from rest_framework import serializers, status, viewsets
from rest_framework.response import Response

from apps.requesters.models import Requester
from apps.requesters.selectors import requesters_list


class RequesterListView(viewsets.GenericViewSet):
    class OutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = Requester
            fields = [
                'id',
                'name',
            ]

    def list(self, request):
        requesters = requesters_list()
        response_data = self.OutputSerializer(requesters, many=True).data

        return Response(response_data, status=status.HTTP_200_OK)
