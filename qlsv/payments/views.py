from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Sum, F, DecimalField
from .models import Enrollment, StudentPayment

def calculate_student_semester_fees(student):
    # Tính tổng học phí dựa trên môn đã đăng ký
    fees = (
        Enrollment.objects
        .filter(student=student)
        .select_related('class_obj__course', 'class_obj__semester')
        .values(
            'class_obj__semester__semester_id',
            'class_obj__semester__year',
            'class_obj__semester__term'
        )
        .annotate(
            total_fee=Sum(F('class_obj__course__credit') * F('class_obj__semester__credit_fee'), output_field=DecimalField())
        )
    )

    result = []
    for f in fees:
        semester_id = f['class_obj__semester__semester_id']
        # Lấy thông tin đã đóng từ StudentPayments (nếu có)
        payment = StudentPayment.objects.filter(student=student, semester_id=semester_id).first()
        paid_amount = payment.paid_amount if payment else 0
        remaining_amount = f['total_fee'] - paid_amount

        result.append({
            'semester_id': semester_id,
            'year': f['class_obj__semester__year'],
            'term': f['class_obj__semester__term'],
            'total_fee': f['total_fee'],
            'paid_amount': paid_amount,
            'remaining_amount': remaining_amount
        })

    return result





@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def student_semester_fees(request):
    student = request.user.student  # giả sử mối quan hệ Account -> Student đã có
    # print(student)
    fees = calculate_student_semester_fees(student)
    return Response(fees)
