from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles(models.IntegerChoices):
    READ_ONLY = 1, 'Только просмотр записей'
    READ_WRITE_EDIT = 2, 'Просмотр, создание и редактирование записей'
    READ_WRITE_EDIT_DELETE = 3, 'Просмотр, создание редактирование и удаление записей'
    ADMIN = 10, 'Администратор'

    @classmethod
    def get_role_list(cls, role):
        return {
            cls.READ_ONLY: ['read'],
            cls.READ_WRITE_EDIT: ['read', 'write', 'edit'],
            cls.READ_WRITE_EDIT_DELETE: ['read', 'write', 'edit', 'delete'],
            cls.ADMIN: ['read', 'write', 'edit', 'delete', 'admin'],
        }[role]


class User(AbstractUser):
    role = models.PositiveIntegerField(
        'Права пользователя',
        choices=UserRoles.choices,
        default=UserRoles.READ_ONLY,
    )
