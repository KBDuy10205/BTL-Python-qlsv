from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Student
from django.contrib.auth.hashers import make_password
from account.models import Account


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

    def save_model(self, request, obj, form, change):
        """
        Khi thêm sinh viên mới qua trang admin:
        - Nếu chưa có account tương ứng, tự tạo account mới.
        - Gán account đó cho student.
        """
        if not obj.account:
            # Nếu sinh viên chưa có tài khoản thì tự tạo
            if not Account.objects.filter(email=obj.email).exists():
                hashed_pw = make_password("123456")  # mật khẩu mặc định
                account = Account.objects.create(
                    email=obj.email,
                    password=hashed_pw,
                    role='Student'
                )
                obj.account = account
            else:
                # Nếu tài khoản đã tồn tại thì gán account đó
                obj.account = Account.objects.get(email=obj.email)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Khi xóa Student -> xóa luôn Account liên kết
        """
        if obj.account:
            obj.account.delete()
        super().delete_model(request, obj)
