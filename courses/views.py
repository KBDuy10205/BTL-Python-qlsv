# Trong courses/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import openpyxl
# Đảm bảo import IntegrityError để xử lý lỗi khóa chính bị trùng
from django.db import transaction, IntegrityError
from .models import Course, Faculty
from .serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    # Cấu hình chung
    queryset = Course.objects.all().select_related('Faculty')
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['CourseName', '=CourseID']

    # ===================================================================
    # 1.  THÊM (CREATE)
    # ===================================================================
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)

                return Response({
                    'status': 'success',
                    'message': f'Thêm môn học "{serializer.instance.CourseName}" (Mã: {serializer.instance.CourseID}) thành công!',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)

            except IntegrityError:
                # Xử lý lỗi khi CourseID bị trùng lặp
                return Response({
                    'status': 'error',
                    'message': 'Lỗi: Mã môn học này đã tồn tại. Vui lòng chọn mã khác.',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'status': 'error',
            'message': 'Dữ liệu đầu vào không hợp lệ.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # ===================================================================
    # 2.  SỬA (UPDATE)
    # ===================================================================
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        course_id = instance.CourseID

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'status': 'success',
            'message': f'Cập nhật môn học "{instance.CourseName}" (Mã: {course_id}) thành công!',
            'data': serializer.data
        })

    # ===================================================================
    # 3. GHI ĐÈ XÓA (DESTROY)
    # ===================================================================
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        course_name = instance.CourseName
        course_id = instance.CourseID

        self.perform_destroy(instance)

        return Response({
            'status': 'success',
            'message': f'Xóa môn học "{course_name}" (Mã: {course_id}) thành công!'
        }, status=status.HTTP_204_NO_CONTENT)

    # ===================================================================
    # 4. Thêm môn học từ Excel
    # ===================================================================
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
                    # Giả định thứ tự cột: Tên môn, Tín chỉ, ID Khoa
                    course_name = row[0]
                    credit = row[1]
                    faculty_id = row[2]

                    # Giả định nếu CourseID là nhập tay, nó sẽ là row[3].
                    # Tùy chỉnh dòng này nếu cấu trúc file Excel của bạn khác.
                    course_id = row[3] if len(row) > 3 else None

                    if not (course_name and credit and faculty_id):
                        continue

                    try:
                        faculty = Faculty.objects.get(pk=faculty_id)

                        # Tạo dictionary chứa dữ liệu, chỉ thêm CourseID nếu nó tồn tại
                        course_data = {
                            'CourseName': course_name,
                            'Credit': int(credit),
                            'Faculty': faculty
                        }
                        if course_id:
                            course_data['CourseID'] = course_id

                        new_courses.append(Course(**course_data))

                    except Faculty.DoesNotExist:
                        continue

                Course.objects.bulk_create(new_courses)

            return Response({'message': f'Đã thêm thành công {len(new_courses)} môn học.'},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Lỗi khi xử lý file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)