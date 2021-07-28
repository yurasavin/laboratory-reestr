from apps.users.models import User


def users_list():
    return User.objects.filter(is_superuser=False)
