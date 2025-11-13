from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal, ROUND_HALF_UP

class Score(models.Model):
    StudentCode = models.CharField(max_length=32, verbose_name="Mã sinh viên")
    CourseId = models.CharField(max_length=32, verbose_name ="Mã môn học")

    WeightAttendance = models.DecimalField(
        max_digits=3, decimal_places=2, default=Decimal('0.1'),
        verbose_name="Trọng số chuyên cần"
    )
    WeightMidterm = models.DecimalField(
        max_digits=3, decimal_places=2, default=Decimal('0.2'),
        verbose_name="Trọng số giữa kỳ"
    )
    WeightFinal = models.DecimalField(
        max_digits=3, decimal_places=2, default=Decimal('0.7'),
        verbose_name="Trọng số cuối kỳ"
    )

    Attendance = models.DecimalField(
        max_digits=4, decimal_places=2, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="Điểm chuyên cần"
    )
    Midterm = models.DecimalField(
        max_digits=4, decimal_places=2, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="Điểm giữa kỳ"
    )
    Final = models.DecimalField(
        max_digits=4, decimal_places=2, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="Điểm cuối kỳ"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Scores"
        indexes = [
            models.Index(fields=["StudentCode"]),
            models.Index(fields=["CourseId"]),
        ]
        ordering = ["StudentCode", "CourseId"]

    @property
    def Total(self):
        total_score = (
            (self.Attendance * self.WeightAttendance) +
            (self.Midterm * self.WeightMidterm) +
            (self.Final * self.WeightFinal)
        )
        return total_score.quantize(
            Decimal('0.01'), 
            rounding=ROUND_HALF_UP
        )

    def __str__(self):
        return f"{self.StudentCode} - {self.CourseId} : {self.Total}"
