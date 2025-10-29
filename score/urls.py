from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScoreViewSet, score_dashboard

router = DefaultRouter()
router.register(r"scores", ScoreViewSet, basename="scores")

urlpatterns = [
    path("", include(router.urls)),          
    path("dashboard/", score_dashboard, name="score_dashboard"),
]
