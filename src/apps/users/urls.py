from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views

from apps.users import apis

router = routers.SimpleRouter()
router.register('users', apis.UserGetMeView, basename='users')
router.register('users', apis.UserListView, basename='users')
router.register('users/create', apis.UserCreateView, basename='users')
router.register('users', apis.UserPatchView, basename='users')
router.register('users', apis.UserPasswordChangeView, basename='users')

urlpatterns = [
    path('auth/login/', views.obtain_auth_token),
] + router.urls
