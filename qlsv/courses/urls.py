# Trong courses/urls.py (của app)
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet # Import ViewSet từ views.py cùng thư mục

router = DefaultRouter()
# Tạo endpoint API cho module Môn học
router.register(r'', CourseViewSet, basename='course')

urlpatterns = router.urls
