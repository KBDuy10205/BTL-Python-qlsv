from django.contrib import admin
from .models import Student, Course, Score

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("code","full_name")
    search_fields = ("code","full_name")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code","name","credits")
    search_fields = ("code","name")

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("student","course","midterm","final","other","total")
    list_filter = ("course",)
    search_fields = ("student__code","student__full_name","course__code","course__name")
