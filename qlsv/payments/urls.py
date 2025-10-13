from django.urls import path
from .views import student_semester_fees

urlpatterns = [
    path('student/semester-fees', student_semester_fees, name='student-semester-fees'),
]