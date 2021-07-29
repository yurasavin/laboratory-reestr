from rest_framework import routers

from apps.researches import apis

router = routers.SimpleRouter()
router.register('researches', apis.ResearchListView, basename='researches')
router.register('researches/create', apis.ResearchCreateView, basename='researches')  # noqa: #501
router.register('researches', apis.ResearchPatchView, basename='researches')
router.register('researches', apis.ResearchRemoveView, basename='researches')
router.register('researches', apis.ResearchExportView, basename='researches')
router.register('researches', apis.ResearchStatsView, basename='researches')

urlpatterns = router.urls
