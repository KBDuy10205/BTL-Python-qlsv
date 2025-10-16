from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    code = models.CharField(max_length=32, unique=True)
    full_name = models.CharField(max_length=128)
    class Meta:
        ordering = ["code"]
    def __str__(self): return f"{self.code} - {self.full_name}"

class Course(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128)
    credits = models.PositiveIntegerField(default=3)
    class Meta:
        ordering = ["code"]
    def __str__(self): return f"{self.code} - {self.name}"

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="scores")
    course  = models.ForeignKey(Course,  on_delete=models.CASCADE, related_name="scores")
    midterm = models.DecimalField(max_digits=4, decimal_places=2,
                                  validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
    final   = models.DecimalField(max_digits=4, decimal_places=2,
                                  validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
    other   = models.DecimalField(max_digits=4, decimal_places=2,
                                  validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
    # trọng số mặc định: GK 40% + CK 60%, có thể tùy biến ở settings
    weight_midterm = models.DecimalField(max_digits=4, decimal_places=2, default=0.4)
    weight_final   = models.DecimalField(max_digits=4, decimal_places=2, default=0.6)
    weight_other   = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    class Meta:
        unique_together = ("student", "course")
        indexes = [models.Index(fields=["student"]), models.Index(fields=["course"])]

    @property
    def total(self):
        def v(x): return float(x) if x is not None else 0.0
        return round(
            v(self.midterm)*float(self.weight_midterm) +
            v(self.final)*float(self.weight_final) +
            v(self.other)*float(self.weight_other), 2
        )

    def __str__(self): return f"{self.student.code}-{self.course.code}: {self.total}"
