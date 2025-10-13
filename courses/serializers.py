# Trong courses/serializers.py
from rest_framework import serializers
from .models import Course, Faculty  # Model Faculty đã được import ở đây


# Serializer phụ cho Faculty (để hiển thị tên khoa khi GET)
class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('FacultyID', 'FacultyName')


# Serializer chính cho Course
class CourseSerializer(serializers.ModelSerializer):
    # Đổi tên trường hiển thị Faculty thành 'faculty_details' hoặc tương tự
    faculty_details = FacultySerializer(source='Faculty', read_only=True)

    # Dùng cho hoạt động WRITE (POST/PUT): vẫn trỏ đến Model Faculty
    FacultyID = serializers.PrimaryKeyRelatedField(
        # KHẮC PHỤC LỖI: Gọi đúng Model Faculty đã import
        queryset=Faculty.objects.all(),
        source='Faculty',
        write_only=True,
        required=True
    )

    class Meta:
        model = Course
        # fields list các trường muốn hiển thị và xử lý
        fields = ('CourseID', 'CourseName', 'Credit', 'faculty_details', 'FacultyID')
        read_only_fields = ('CourseID',)