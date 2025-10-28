from rest_framework import serializers
from .models import Score

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
        extra_kwargs = {
            "StudentCode": {"label": "Mã sinh viên"},
            "FullName": {"label": "Họ và tên"},
            "CourseName": {"label": "Tên học phần"},
            "Midterm": {"label": "Điểm giữa kỳ"},
            "Final": {"label": "Điểm cuối kỳ"},
            "Other": {"label": "Điểm khác"},
            "WeightMidterm": {"label": "Trọng số giữa kỳ"},
            "WeightFinal": {"label": "Trọng số cuối kỳ"},
            "WeightOther": {"label": "Trọng số khác"},
        }

class ManualScoreEditSerializer(serializers.Serializer):
    StudentCode = serializers.CharField(label="Mã sinh viên", required=True)
    FullName = serializers.CharField(label="Họ và tên", required=False)
    CourseName = serializers.CharField(label="Tên học phần", required=True)
    Midterm = serializers.DecimalField(label="Điểm giữa kỳ", max_digits=4, decimal_places=2, required=False)
    Final = serializers.DecimalField(label="Điểm cuối kỳ", max_digits=4, decimal_places=2, required=False)
    Other = serializers.DecimalField(label="Điểm khác", max_digits=4, decimal_places=2, required=False)
    WeightMidterm = serializers.DecimalField(label="Trọng số giữa kỳ", max_digits=4, decimal_places=2, required=False)
    WeightFinal = serializers.DecimalField(label="Trọng số cuối kỳ", max_digits=4, decimal_places=2, required=False)
    WeightOther = serializers.DecimalField(label="Trọng số khác", max_digits=4, decimal_places=2, required=False)

    def validate(self, attrs):
        if not attrs.get("StudentCode"):
            raise serializers.ValidationError("Thiếu mã sinh viên.")
        if not attrs.get("CourseName"):
            raise serializers.ValidationError("Thiếu tên học phần.")
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        score, _ = Score.objects.get_or_create(
            StudentCode=data["StudentCode"],
            CourseName=data["CourseName"],
            defaults={"FullName": data.get("FullName", "")},
        )
        for field in [
            "FullName", "Midterm", "Final", "Other",
            "WeightMidterm", "WeightFinal", "WeightOther"
        ]:
            if field in data and data[field] is not None:
                setattr(score, field, data[field])
        score.save()
        return score
