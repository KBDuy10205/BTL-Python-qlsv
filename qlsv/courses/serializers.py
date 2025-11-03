# Trong courses/serializers.py
from rest_framework import serializers
from .models import Course # Model Faculty đã được import ở đây



# Serializer chính cho Course
class CourseSerializer(serializers.ModelSerializer):


    class Meta:
        model = Course
        # fields list các trường muốn hiển thị và xử lý
        fields = ('CourseID', 'CourseName', 'Credit')