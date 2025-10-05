from django.contrib import admin
from import_export.admin import ImportExportModelAdmin  # nếu dùng import/export
from .models import Student

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):  # hoặc admin.ModelAdmin nếu chưa cài import-export
    list_display = ('id', 'full_name', 'email', 'phone', 'major_id', 'admission_year')
    search_fields = ('id', 'full_name', 'email', 'phone')
