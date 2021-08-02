from rest_framework import routers

from apps.requesters import apis

router = routers.SimpleRouter()
router.register('requesters', apis.RequesterListView, basename='requesters')

urlpatterns = router.urls
