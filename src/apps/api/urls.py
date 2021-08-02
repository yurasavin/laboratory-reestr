from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path('auth/login/', views.obtain_auth_token),
    path('', include(('apps.users.urls'))),
    path('', include(('apps.researches.urls'))),
    path('', include(('apps.requesters.urls'))),
]
