from apps.users.models import User


def user_create(*, user_data):
    password = user_data.pop('password')

    user = User(**user_data)
    user.set_password(password)
    user.save()

    return user


def user_patch(*, user_data):
    user = User.objects.filter(id=user_data.pop('id'))
    user.update(**user_data)

    return user.get()


def user_password_change(*, user_data):
    user = User.objects.get(id=user_data['id'])
    user.set_password(user_data['password'])
    user.save()
