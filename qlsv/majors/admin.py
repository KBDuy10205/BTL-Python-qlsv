from django.contrib import admin
from .models import Major

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('major_id', 'major_name', 'faculty_name')
    search_fields = ('major_name',)
