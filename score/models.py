from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Score(models.Model):
    StudentCode = models.CharField(max_length=32, verbose_name="Mã sinh viên")
    FullName    = models.CharField(max_length=128, verbose_name="Họ và tên", blank=True, default="")
    CourseName  = models.CharField(max_length=128, verbose_name="Tên học phần")
    Attendance = models.FloatField(default=0)  # điểm chuyên cần 10%
    Midterm = models.FloatField(default=0)
    Final = models.FloatField(default=0)
    Other = models.FloatField(default=0)
    WeightAttendance = models.FloatField(default=0.1)  # 10%
    WeightMidterm = models.FloatField(default=0.2)     # 20%
    WeightFinal = models.FloatField(default=0.7)       # 70%

    Attendance  = models.DecimalField(  # 10%
        max_digits=4, decimal_places=2, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="Điểm chuyên cần"
    )
    Midterm     = models.DecimalField(  # 20%
        max_digits=4, decimal_places=2, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="Điểm giữa kỳ"
    )
    Final       = models.DecimalField(  # 70%
        max_digits=4, decimal_places=2, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="Điểm cuối kỳ"
    )

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Scores"
        indexes = [
            models.Index(fields=["StudentCode"]),
            models.Index(fields=["CourseName"]),
        ]
        ordering = ["StudentCode", "CourseName"]

    @property
    def Total(self):
        a = float(self.Attendance or 0)
        m = float(self.Midterm or 0)
        f = float(self.Final or 0)
        return round(0.10 * a + 0.20 * m + 0.70 * f, 2)

    def __str__(self):
        return f"{self.StudentCode} - {self.CourseName} : {self.Total}"
