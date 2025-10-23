from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Nếu đã có Faculty ở app khác thì import từ đó và XÓA model dưới.
class Faculty(models.Model):
    FacultyID = models.AutoField(primary_key=True)
    FacultyName = models.CharField(max_length=100)

    class Meta:
        db_table = 'Faculties'
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return f"{self.FacultyID} - {self.FacultyName}"


# --- Model CHÍNH theo yêu cầu: Course ---
class Course(models.Model):
    CourseID = models.AutoField(primary_key=True)
    CourseName = models.CharField(max_length=100)
    Credit = models.IntegerField()
    # Khóa ngoại đến Faculty (yêu cầu thường dùng PROTECT để không xóa dây chuyền)
    Faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, db_column='FacultyID')

    class Meta:
        db_table = 'Courses'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['CourseID']

    def __str__(self):
        return f"{self.CourseID} - {self.CourseName}"


# Nếu trước đó bạn đã có Student kiểu khác thì giữ nguyên. Đây là bản tối giản.
class Student(models.Model):
    StudentID = models.AutoField(primary_key=True)
    StudentCode = models.CharField(max_length=32, unique=True)
    FullName = models.CharField(max_length=128)

    class Meta:
        db_table = 'Students'
        ordering = ['StudentCode']

    def __str__(self):
        return f"{self.StudentCode} - {self.FullName}"


# Cập nhật Score để tham chiếu Course mới
class Score(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='StudentID', related_name='Scores')
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='CourseID', related_name='Scores')

    Midterm = models.DecimalField(max_digits=4, decimal_places=2,
                                  validators=[MinValueValidator(0), MaxValueValidator(10)],
                                  null=True, blank=True)
    Final = models.DecimalField(max_digits=4, decimal_places=2,
                                validators=[MinValueValidator(0), MaxValueValidator(10)],
                                null=True, blank=True)
    Other = models.DecimalField(max_digits=4, decimal_places=2,
                                validators=[MinValueValidator(0), MaxValueValidator(10)],
                                null=True, blank=True)

    WeightMidterm = models.DecimalField(max_digits=4, decimal_places=2, default=0.4)
    WeightFinal   = models.DecimalField(max_digits=4, decimal_places=2, default=0.6)
    WeightOther   = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    class Meta:
        db_table = 'Scores'
        unique_together = (('Student', 'Course'),)
        indexes = [models.Index(fields=['Student']), models.Index(fields=['Course'])]

    @property
    def Total(self):
        v = lambda x: float(x) if x is not None else 0.0
        return round(
            v(self.Midterm)*float(self.WeightMidterm) +
            v(self.Final)*float(self.WeightFinal) +
            v(self.Other)*float(self.WeightOther), 2
        )

    def __str__(self):
        return f"{self.Student.StudentCode}-{self.Course.CourseName}: {self.Total}"
