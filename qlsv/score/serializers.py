from rest_framework import serializers
from .models import Student, Course, Score

class ManualScoreEditSerializer(serializers.Serializer):
    # nhận theo code cho dễ, vẫn hỗ trợ ID nếu bạn gửi
    student_code = serializers.CharField(required=False, allow_blank=False)
    course_code  = serializers.CharField(required=False, allow_blank=False)
    student_id   = serializers.IntegerField(required=False)
    course_id    = serializers.IntegerField(required=False)

    midterm = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)
    final   = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)
    other   = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)

    weight_midterm = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)
    weight_final   = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)
    weight_other   = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)

    def validate(self, attrs):
        # ít nhất phải có định danh SV + HP
        if not any(k in attrs for k in ("student_id","student_code")):
            raise serializers.ValidationError("Thiếu student_id hoặc student_code")
        if not any(k in attrs for k in ("course_id","course_code")):
            raise serializers.ValidationError("Thiếu course_id hoặc course_code")
        return attrs

    def save(self, **kwargs):
        data = self.validated_data

        # tìm student
        if "student_id" in data:
            student = Student.objects.get(pk=data["student_id"])
        else:
            student = Student.objects.get(StudentCode=data["student_code"])

        # tìm course
        if "course_id" in data:
            course = Course.objects.get(pk=data["course_id"])
        else:
            course = Course.objects.get(CourseName=data["course_code"]) if hasattr(Course, "CourseName") and not hasattr(Course, "code") else Course.objects.get(CourseID=data["course_id"])  # fallback
            # Nếu bạn dùng CourseCode riêng, đổi dòng trên cho đúng field của bạn.

        # lấy score hiện có
        score, _ = Score.objects.get_or_create(Student=student, Course=course)

        # cập nhật các trường được gửi lên
        fields = ["midterm","final","other","weight_midterm","weight_final","weight_other"]
        mapping = {
            "midterm": "Midterm", "final": "Final", "other": "Other",
            "weight_midterm": "WeightMidterm", "weight_final": "WeightFinal", "weight_other": "WeightOther"
        }
        for f in fields:
            if f in data and data[f] is not None:
                setattr(score, mapping[f], data[f])
        score.save()
        return score
