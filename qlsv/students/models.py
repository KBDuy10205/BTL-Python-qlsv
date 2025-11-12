from django.db import models
from django.conf import settings  # dùng để tránh vòng lặp import
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from majors.models import Major
from account.models import Account  # import model Account
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist


class Student(models.Model):
    # Khóa chính
    student_id = models.CharField(max_length = 10, primary_key=True, db_column='StudentID')

    # Liên kết 1-1 với Account
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='AccountID',
        related_name='student_profile',
        null=True, blank=True,
    )

    full_name = models.CharField(max_length=50, db_column='FullName')
    gender = models.CharField(max_length=10,choices=[('Nữ','Nữ'),('Nam','Nam')],null=True, blank=True, db_column='Gender')
    birth_date = models.DateField(null=True, blank=True, db_column='BirthDate')
    email = models.EmailField(max_length=100, unique=True, db_column='Email')
    phone = models.CharField(max_length=15, null=True, blank=True, db_column='Phone')
    address = models.CharField(max_length=100, null=True, blank=True, db_column='Address')

    major = models.ForeignKey(
        Major, on_delete=models.SET_NULL, null=True, db_column='MajorID'
    )

    admission_year = models.IntegerField(null=True, blank=True, db_column='AdmissionYear')

    class Meta:
        db_table = 'Students'
        ordering = ['student_id']

    def __str__(self):
        # Tránh lỗi nếu account chưa gán
        return f"{self.full_name} ({self.account.email if self.account else 'No Account'})"


# =====================================================
# 🧩 SIGNALS: Tự động tạo / xóa tài khoản cho sinh viên
# =====================================================

@receiver(post_save, sender=Student)
def create_account_for_student(sender, instance, created, **kwargs):
    """
    Khi tạo sinh viên mới -> tự động tạo tài khoản Account tương ứng.
    """
    if created and not instance.account:
        # tạo user mới trong bảng Accounts
        hashed_pw = make_password("123456")
        account = Account.objects.create_user(
            email=instance.email,
            password=hashed_pw,  # mật khẩu mặc định
            role='Student'
        )
        instance.account = account
        instance.save()


@receiver(post_delete, sender=Student)
def delete_account_for_student(sender, instance, **kwargs):
    try:
        if instance.account_id:  # chỉ kiểm tra ID, không load object
            instance.account.delete()
    except ObjectDoesNotExist:
        # Account đã bị xóa từ trước thì bỏ qua
        pass