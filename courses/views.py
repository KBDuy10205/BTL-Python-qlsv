# Trong courses/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import openpyxl
from django.db import transaction
from .models import Course, Faculty  # Import models
from .serializers import CourseSerializer  # Import serializer


class CourseViewSet(viewsets.ModelViewSet):
    # 3. Hiển thị danh sách và thông tin
    # 5. Thêm, Sửa, Xóa (CRUD)
    queryset = Course.objects.all().select_related('Faculty')
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    # 4. Tìm kiếm môn học theo Mã môn, Tên môn
    filter_backends = [filters.SearchFilter]
    search_fields = ['CourseName', '=CourseID']

    # 6. Thêm môn học từ Excel
    @action(detail=False, methods=['post'], url_path='upload-excel')
    def upload_courses_excel(self, request):
        excel_file = request.FILES.get('file')
        if not excel_file:
            return Response({'error': 'Vui lòng cung cấp file Excel.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            workbook = openpyxl.load_workbook(excel_file)
            sheet = workbook.active
            new_courses = []

            with transaction.atomic():
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    course_name = row[0]
                    credit = row[1]
                    faculty_id = row[2]

                    if not (course_name and credit and faculty_id):
                        continue

                    try:
                        faculty = Faculty.objects.get(pk=faculty_id)
                        new_courses.append(
                            Course(CourseName=course_name, Credit=int(credit), Faculty=faculty)
                        )
                    except Faculty.DoesNotExist:
                        continue

                Course.objects.bulk_create(new_courses)

            return Response({'message': f'Đã thêm thành công {len(new_courses)} môn học.'},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Lỗi khi xử lý file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)