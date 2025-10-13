# Trong course/urls.py (của project)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dòng này nhúng các API của module Môn học
    path('api/', include('courses.urls')),
]