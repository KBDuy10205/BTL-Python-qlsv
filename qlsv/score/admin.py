from django.contrib import admin
from .models import Score

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("StudentCode", "CourseId", "Attendance", "Midterm", "Final", "Total")
    search_fields = ("StudentCode",  "CourseId")
    list_editable = ("Attendance", "Midterm", "Final")
    readonly_fields = ()