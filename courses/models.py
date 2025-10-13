from django.db import models


# --- Model Phụ thuộc: Faculty ---
class Faculty(models.Model):
    FacultyID = models.AutoField(primary_key=True)
    FacultyName = models.CharField(max_length=100)
    Office = models.CharField(max_length=100)
    Phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'Faculties'

    def __str__(self):
        return self.FacultyName


# --- Model Chính: Course (Công việc của bạn) ---
class Course(models.Model):
    CourseID = models.AutoField(primary_key=True)
    CourseName = models.CharField(max_length=100)
    Credit = models.IntegerField()

    # Khóa ngoại đến Faculty.
    Faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)

    class Meta:
        db_table = 'Courses'
        verbose_name = 'Course'

    def __str__(self):
        return f"{self.CourseID} - {self.CourseName}"