from django.contrib import admin

from .models import (
    Semester,
    StudentPayment,
    Faculty,
    Course,
    MajorCourse,
    Lecturer,
    Schedule,
    Class,
    Enrollment
)

# Register your models here
admin.site.register(Semester)
admin.site.register(StudentPayment)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(MajorCourse)
admin.site.register(Lecturer)
admin.site.register(Schedule)
admin.site.register(Class)
admin.site.register(Enrollment)
