from django.contrib import admin
from .models import Score

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("StudentCode", "FullName", "CourseName", "Attendance", "Midterm", "Final", "Total")
    search_fields = ("StudentCode", "FullName", "CourseName")
    list_editable = ("Attendance", "Midterm", "Final")
    readonly_fields = ()
