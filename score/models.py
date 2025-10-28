from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Score(models.Model):
    StudentCode = models.CharField(max_length=32)
    FullName = models.CharField(max_length=128, blank=True, default="")
    CourseName = models.CharField(max_length=100)
    Midterm = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
    Final = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
    Other = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
    WeightMidterm = models.DecimalField(max_digits=4, decimal_places=2, default=0.4)
    WeightFinal = models.DecimalField(max_digits=4, decimal_places=2, default=0.6)
    WeightOther = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Scores"
        unique_together = (("StudentCode", "CourseName"),)
        indexes = [models.Index(fields=["StudentCode"]), models.Index(fields=["CourseName"])]
        ordering = ["StudentCode", "CourseName"]

    @property
    def Total(self):
        v = lambda x: float(x) if x is not None else 0.0
        return round(v(self.Midterm) * float(self.WeightMidterm) + v(self.Final) * float(self.WeightFinal) + v(self.Other) * float(self.WeightOther), 2)

    def __str__(self):
        return f"{self.StudentCode} - {self.CourseName}: {self.Total}"
