from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Student


# Resource cho import/export Excel
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        import_id_fields = ['email']
        fields = (
            'student_id', 'full_name', 'email', 'phone',
            'gender', 'birth_date', 'major_id', 'admission_year'
        )


# Đăng ký model vào admin
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('student_id', 'full_name', 'email', 'phone', 'major_id', 'admission_year')
    search_fields = ('student_id', 'full_name', 'email', 'phone')
