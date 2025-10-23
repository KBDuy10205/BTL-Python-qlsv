from django.contrib import admin
from .models import Faculty, Course, Student, Score

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("FacultyID","FacultyName")
    search_fields = ("FacultyName",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("CourseID","CourseName","Credit","Faculty")
    search_fields = ("CourseName",)
    list_filter = ("Faculty",)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("StudentID","StudentCode","FullName")
    search_fields = ("StudentCode","FullName")

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("Student","Course","Midterm","Final","Other","Total")
    list_filter = ("Course",)
    search_fields = ("Student__StudentCode","Student__FullName","Course__CourseName")
