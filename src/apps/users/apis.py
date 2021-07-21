from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import User, UserRoles


class UserGetMeView(viewsets.ViewSet):
    class OutputSerializer(serializers.ModelSerializer):
        roles = serializers.SerializerMethodField()
        name = serializers.SerializerMethodField()

        class Meta:
            model = User
            fields = ['id', 'name', 'roles']

        def get_roles(self, instance):
            return UserRoles.get_role_list(instance.role)

        def get_name(self, instance):
            return instance.get_full_name()

    @action(detail=False)
    def me(self, request):
        serializer = self.OutputSerializer(request.user)
        return Response(serializer.data)
