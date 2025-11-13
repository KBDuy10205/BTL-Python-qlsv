from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Score
from decimal import Decimal

class ScoreSerializer(serializers.ModelSerializer):
    Total = serializers.ReadOnlyField()

    class Meta:
        model = Score
        fields = [
            'id', 'StudentCode', 'CourseId', 
            'WeightAttendance', 'WeightMidterm', 'WeightFinal',
            'Attendance', 'Midterm', 'Final',
            'Total', 'created_at', 'updated_at' 
        ]
        read_only_fields = ['Total', 'created_at', 'updated_at']


class ManualScoreEditSerializer(serializers.Serializer):
    StudentCode = serializers.CharField(label="Mã sinh viên", required=True)
    CourseId = serializers.CharField(label="Mã học phần", required=True)

    Attendance = serializers.DecimalField(
        label="Điểm chuyên cần", max_digits=4, decimal_places=2, required=False,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    Midterm = serializers.DecimalField(
        label="Điểm giữa kỳ", max_digits=4, decimal_places=2, required=False,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    Final = serializers.DecimalField(
        label="Điểm cuối kỳ", max_digits=4, decimal_places=2, required=False,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    
    WeightAttendance = serializers.DecimalField(
        label="Trọng số chuyên cần", max_digits=3, decimal_places=2, required=False,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    WeightMidterm = serializers.DecimalField(
        label="Trọng số giữa kỳ", max_digits=3, decimal_places=2, required=False,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    WeightFinal = serializers.DecimalField(
        label="Trọng số cuối kỳ", max_digits=3, decimal_places=2, required=False,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    def save(self, **kwargs):
        data = self.validated_data
        
        score, created = Score.objects.get_or_create(
            StudentCode=data["StudentCode"],
            CourseId=data["CourseId"],
            defaults={}
        )
        
        update_fields = [
            "Attendance", "Midterm", "Final",
            "WeightAttendance", "WeightMidterm", "WeightFinal"
        ]
        
        has_updates = False
        for field in update_fields:
            if field in data and data[field] is not None:
                setattr(score, field, data[field])
                has_updates = True
        
        if created or has_updates:
            score.save()
            
        return score
