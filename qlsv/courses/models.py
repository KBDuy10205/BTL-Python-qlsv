from django.db import models


# --- Model Chính: Course (Công việc của bạn) ---
class Course(models.Model):
    CourseID = models.CharField(max_length=15, primary_key=True)
    CourseName = models.CharField(max_length=100)
    Credit = models.IntegerField()

    class Meta:
        db_table = 'Courses'
        verbose_name = 'Course'

    def __str__(self):
        return f"{self.CourseID} - {self.CourseName}"