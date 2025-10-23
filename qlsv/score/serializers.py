from rest_framework import serializers
from .models import Student, Course, Score

class StudentSerializer(serializers.ModelSerializer):
    class Meta: model = Student; fields = ["id","code","full_name"]

class CourseSerializer(serializers.ModelSerializer):
    class Meta: model = Course; fields = ["id","code","name","credits"]

class ScoreSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course  = CourseSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source="student", write_only=True)
    course_id  = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source="course", write_only=True)
    total = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)

    class Meta:
        model = Score
        fields = ["id","student","course","student_id","course_id",
                  "midterm","final","other","weight_midterm","weight_final","weight_other","total"]
