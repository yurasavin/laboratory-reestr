from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.api.permissions import AdminPermission
from apps.users.models import User, UserRoles
from apps.users.selectors import users_list
from apps.users.services import user_create, user_password_change, user_patch


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


class UserListView(viewsets.ViewSet):
    class OutputSerializer(serializers.ModelSerializer):
        role_display = serializers.SerializerMethodField()

        class Meta:
            model = User
            fields = [
                'id', 'first_name', 'last_name', 'username', 'role',
                'role_display', 'is_active',
            ]

        def get_role_display(self, instance):
            return instance.get_role_display()

    def list(self, request):
        users = users_list()
        serializer = self.OutputSerializer(users, many=True)
        return Response(serializer.data)


class UserCreateView(viewsets.ViewSet):
    permission_classes = [AdminPermission]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                'first_name', 'last_name', 'username', 'password', 'role',
                'is_active',
            ]

    class OutputSerializer(serializers.ModelSerializer):
        role_display = serializers.SerializerMethodField()

        class Meta:
            model = User
            fields = [
                'id', 'first_name', 'last_name', 'username', 'role',
                'role_display', 'is_active',
            ]

        def get_role_display(self, instance):
            return instance.get_role_display()

    def create(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        user = user_create(user_data=input_serializer.validated_data)

        output_serializer = self.OutputSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class UserPatchView(viewsets.ViewSet):
    permission_classes = [AdminPermission]

    class InputSerializer(serializers.ModelSerializer):
        id = serializers.IntegerField()

        class Meta:
            model = User
            fields = [
                'id', 'first_name', 'last_name', 'username', 'role',
                'is_active',
            ]

    class OutputSerializer(serializers.ModelSerializer):
        role_display = serializers.SerializerMethodField()

        class Meta:
            model = User
            fields = [
                'id', 'first_name', 'last_name', 'username', 'role',
                'role_display', 'is_active',
            ]

        def get_role_display(self, instance):
            return instance.get_role_display()

    @action(detail=False, methods=['post'])
    def patch(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        user = user_patch(user_data=input_serializer.validated_data)

        output_serializer = self.OutputSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class UserPasswordChangeView(viewsets.ViewSet):
    permission_classes = [AdminPermission]

    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        password = serializers.CharField()

    @action(detail=False, methods=['post'], url_path='password-change')
    def password_change(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        user = user_password_change(user_data=input_serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
