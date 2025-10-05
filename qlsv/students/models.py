from django.db import models

class Student(models.Model):
    # PK int autoincrement -> StudentID
    id = models.AutoField(primary_key=True, db_column='StudentID')

    # (tạm thời để rỗng, sau nối tài khoản sẽ đổi sang ForeignKey)
    account_id = models.IntegerField(null=True, blank=True, db_column='AccountID')

    full_name = models.CharField(max_length=100, db_column='FullName')
    gender = models.CharField(max_length=15, null=True, blank=True, db_column='Gender')
    birth_date = models.DateField(null=True, blank=True, db_column='BirthDate')
    email = models.EmailField(max_length=100, unique=True, db_column='Email')
    phone = models.CharField(max_length=15, null=True, blank=True, db_column='Phone')
    address = models.CharField(max_length=100, null=True, blank=True, db_column='Address')
    major_id = models.IntegerField(null=True, blank=True, db_column='MajorID')
    admission_year = models.IntegerField(null=True, blank=True, db_column='AdmissionYear')

    class Meta:
        db_table = 'Students'           # tên bảng đúng design
        ordering = ['id']

    def __str__(self):
        return f"{self.id} - {self.full_name}"
