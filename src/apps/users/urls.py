from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views

from apps.users.apis import UserGetMeView

router = routers.SimpleRouter()
router.register('users', UserGetMeView, basename='users')

urlpatterns = [
    path('auth/login/', views.obtain_auth_token),
] + router.urls
