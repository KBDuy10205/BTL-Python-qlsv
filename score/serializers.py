from rest_framework import serializers
from .models import Score

class ScoreSerializer(serializers.ModelSerializer):
    Total = serializers.SerializerMethodField(label="Điểm tổng kết")

    class Meta:
        model = Score
        fields = [
            "id",
            "StudentCode", "FullName", "CourseName",
            "Attendance", "Midterm", "Final",
            "Total", "created_at", "updated_at",
        ]
        extra_kwargs = {
            "StudentCode": {"label": "Mã sinh viên"},
            "FullName":    {"label": "Họ và tên"},
            "CourseName":  {"label": "Tên học phần"},
            "Attendance":  {"label": "Điểm chuyên cần (10%)"},
            "Midterm":     {"label": "Điểm giữa kỳ (20%)"},
            "Final":       {"label": "Điểm cuối kỳ (70%)"},
        }

    def get_Total(self, obj):
        return obj.Total

class ManualScoreEditSerializer(serializers.Serializer):
    StudentCode = serializers.CharField(label="Mã sinh viên", required=True)
    FullName    = serializers.CharField(label="Họ và tên", required=False, allow_blank=True)
    CourseName  = serializers.CharField(label="Tên học phần", required=True)

    Attendance  = serializers.DecimalField(label="Điểm chuyên cần (10%)", max_digits=4, decimal_places=2, required=False)
    Midterm     = serializers.DecimalField(label="Điểm giữa kỳ (20%)",   max_digits=4, decimal_places=2, required=False)
    Final       = serializers.DecimalField(label="Điểm cuối kỳ (70%)",    max_digits=4, decimal_places=2, required=False)
