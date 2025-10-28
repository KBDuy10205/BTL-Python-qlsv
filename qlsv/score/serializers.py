from rest_framework import serializers
from .models import Score

class ScoreSerializer(serializers.ModelSerializer):
    Total = serializers.SerializerMethodField()

    class Meta:
        model = Score
        fields = ["id", "StudentCode", "FullName", "CourseName", "Midterm", "Final", "Other", "WeightMidterm", "WeightFinal", "WeightOther", "Total", "created_at", "updated_at"]

    def get_Total(self, obj):
        return obj.Total

class ManualScoreEditSerializer(serializers.Serializer):
    StudentCode = serializers.CharField(required=True)
    CourseName = serializers.CharField(required=True)
    FullName = serializers.CharField(required=False, allow_blank=True)
    Midterm = serializers.DecimalField(max_digits=4, decimal_places=2, required=False, min_value=0, max_value=10)
    Final = serializers.DecimalField(max_digits=4, decimal_places=2, required=False, min_value=0, max_value=10)
    Other = serializers.DecimalField(max_digits=4, decimal_places=2, required=False, min_value=0, max_value=10)
    WeightMidterm = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)
    WeightFinal = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)
    WeightOther = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)
