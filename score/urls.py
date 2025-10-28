from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScoreViewSet

router = DefaultRouter()
router.register(r"scores", ScoreViewSet, basename="scores")

urlpatterns = [
    path("", include(router.urls)),
]
