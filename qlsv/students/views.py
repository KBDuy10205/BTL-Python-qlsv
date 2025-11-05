# Django imports
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth.hashers import make_password

# Third-party imports
import pandas as pd
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response



# Local app imports
from account.models import Account
from .models import Student
from .serializers import StudentSerializer
from payments.models import Enrollment


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('student_id')
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['account__email', 'full_name']

    def perform_create(self, serializer):
        # Tự tạo account khi thêm sinh viên mới
        student_email = serializer.validated_data['email']
        hashed_pw = make_password("123456")
        account = Account.objects.create(
            email = student_email,
            password = hashed_pw,
            role = 'Student',
        )
        serializer.save(account=account)

    def perform_destroy(self, instance):
        try:
            if instance.account_id:
                instance.account.delete()
        except Exception:
            pass
        instance.delete()
    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """
        Xuất danh sách sinh viên ra file Excel.
        """
        qs = self.get_queryset().values()
        df = pd.DataFrame(qs)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=students.xlsx'
        df.to_excel(response, index=False)
        return response
    @action(detail=False, methods=['post'])
    def import_excel(self, request):
        """
        Nhập danh sách sinh viên từ file Excel.
        """
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "Chưa chọn file Excel để import!"}, status=400)

        # Kiểm tra định dạng
        if not (file.name.endswith('.xlsx') or file.name.endswith('.csv')):
            return Response({"error": "Chỉ hỗ trợ file .xlsx hoặc .csv"}, status=400)

        try:
            df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
            required_cols = ['FullName', 'Email']
            for col in required_cols:
                if col not in df.columns:
                    return Response({"error": f"Thiếu cột bắt buộc: {col}"}, status=400)

            created = 0
            with transaction.atomic():
                for _, row in df.iterrows():
                    # tránh trùng email
                    if Student.objects.filter(email=row['Email']).exists():
                        continue
                    Student.objects.create(
                        full_name=row['FullName'],
                        email=row['Email'],
                        gender=row.get('Gender', None),
                        birth_date=row.get('BirthDate', None),
                    )
                    created += 1

            return Response({"message": f"Import thành công {created} sinh viên!"}, status=200)

        except Exception as e:
            return Response({"error": f"Lỗi khi đọc file: {str(e)}"}, status=500)
    @action(detail=True, methods=['get'])
    def timetable(self, request, pk=None):
        student = self.get_object()
        enrollments = Enrollment.objects.filter(student=student).select_related('class_obj__course', 'class_obj__schedule')

        data = [
            {
                "class_name": e.class_obj.class_name,
                "course": e.class_obj.course.course_name,
                "day_of_week": e.class_obj.schedule.day_of_week,
                "room": e.class_obj.schedule.room,
                "start_period": e.class_obj.schedule.start_period,
                "period_count": e.class_obj.schedule.period_count,
            }
            for e in enrollments
        ]
        return Response(data)