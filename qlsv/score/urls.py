from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScoreViewSet, score_dashboard, ImportScoreView, export_scores_to_excel

router = DefaultRouter()
router.register(r"scores", ScoreViewSet, basename="scores")

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/", score_dashboard, name="score_dashboard"),
    path("import/", ImportScoreView.as_view(), name="import_scores"),
    path("export/", export_scores_to_excel, name="export_scores"),
]
