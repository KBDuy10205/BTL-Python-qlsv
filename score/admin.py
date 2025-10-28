from django.contrib import admin
from .models import Score

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("StudentCode", "FullName", "CourseName", "Midterm", "Final", "Other", "WeightMidterm", "WeightFinal", "WeightOther", "Total_Display", "updated_at")
    list_editable = ("Midterm", "Final", "Other", "WeightMidterm", "WeightFinal", "WeightOther")
    search_fields = ("StudentCode", "FullName", "CourseName")
    list_filter = ("CourseName",)
    readonly_fields = ("Total_Display", "created_at", "updated_at")
    ordering = ("StudentCode", "CourseName")

    def Total_Display(self, obj):
        return obj.Total
    Total_Display.short_description = "Total (calculated)"
