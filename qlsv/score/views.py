from django.db.models import Avg, F, ExpressionWrapper, FloatField
from django.http import HttpResponse
from rest_framework import viewsets, permissions, decorators, response, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Student, Course, Score
from .serializers import StudentSerializer, CourseSerializer, ScoreSerializer, ManualScoreEditSerializer
from .utils_excel import import_scores_from_excel, export_scores_to_excel


class IsAuth(permissions.IsAuthenticated):
    pass


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by("StudentCode")
    serializer_class = StudentSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["StudentCode", "FullName"]
    search_fields = ["StudentCode", "FullName"]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("Faculty").all().order_by("CourseID")
    serializer_class = CourseSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["CourseName", "Faculty"]
    search_fields = ["CourseName"]


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related("Student", "Course").all().order_by("Student__StudentCode")
    serializer_class = ScoreSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["Student", "Course"]
    search_fields = ["Student__StudentCode", "Student__FullName", "Course__CourseName"]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @decorators.action(detail=False, methods=["post"], url_path="import_excel")
    def import_excel(self, request):
        upfile = request.FILES.get("file")
        if not upfile:
            return response.Response({"detail": "Thiếu file"}, status=400)
        try:
            info = import_scores_from_excel(upfile)
            return response.Response({"message": "OK", **info}, status=200)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=400)

    @decorators.action(detail=False, methods=["get"], url_path="export_excel")
    def export_excel(self, request):
        qs = self.filter_queryset(self.get_queryset())
        buffer = export_scores_to_excel(qs)
        resp = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        resp["Content-Disposition"] = 'attachment; filename="scores.xlsx"'
        return resp

    @decorators.action(detail=False, methods=["get"], url_path="avg_by_student")
    def avg_by_student(self, request):
        sid = request.query_params.get("student_id")
        expr_total = ExpressionWrapper(
            (F("Midterm") * F("WeightMidterm"))
            + (F("Final") * F("WeightFinal"))
            + (F("Other") * F("WeightOther")),
            output_field=FloatField(),
        )
        qs = Score.objects.all()
        if sid:
            qs = qs.filter(Student_id=sid)
        data = (
            qs.values("Student__StudentID", "Student__StudentCode", "Student__FullName")
            .annotate(avg_total=Avg(expr_total))
            .order_by("Student__StudentCode")
        )
        res = [
            {
                "StudentID": r["Student__StudentID"],
                "StudentCode": r["Student__StudentCode"],
                "FullName": r["Student__FullName"],
                "AverageTotal": round(float(r["avg_total"] or 0), 2),
            }
            for r in data
        ]
        return response.Response(res, status=200)

    @decorators.action(detail=False, methods=["get"], url_path="chart_data")
    def chart_data(self, request):
        course_id = request.query_params.get("course_id")
        qs = self.get_queryset()
        if course_id:
            qs = qs.filter(Course_id=course_id)
        totals = [s.Total for s in qs]
        bins = [0] * 11
        for t in totals:
            i = max(0, min(10, int(round(t))))
            bins[i] += 1
        return response.Response(
            {
                "labels": [str(i) for i in range(11)],
                "counts": bins,
                "count": len(totals),
                "avg": round(sum(totals) / len(totals), 2) if totals else 0.0,
            },
            status=200,
        )

    @decorators.action(detail=False, methods=["post"], url_path="manual_edit")
    def manual_edit(self, request):
        ser = ManualScoreEditSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        student = None
        if "student_id" in data:
            student = Student.objects.filter(pk=data["student_id"]).first()
        elif "student_code" in data:
            student = Student.objects.filter(StudentCode=data["student_code"]).first()
        if not student:
            return response.Response({"detail": "Student không tồn tại"}, status=404)

        course = None
        if "course_id" in data:
            course = Course.objects.filter(pk=data["course_id"]).first()
        elif "course_name" in data:
            course = Course.objects.filter(CourseName=data["course_name"]).first()
        if not course:
            return response.Response({"detail": "Course không tồn tại"}, status=404)

        score, _ = Score.objects.get_or_create(Student=student, Course=course)
        mapping = {
            "midterm": "Midterm",
            "final": "Final",
            "other": "Other",
            "weight_midterm": "WeightMidterm",
            "weight_final": "WeightFinal",
            "weight_other": "WeightOther",
        }
        for k_api, k_model in mapping.items():
            if k_api in data and data[k_api] is not None:
                setattr(score, k_model, data[k_api])
        score.save()
        return response.Response(ScoreSerializer(score).data, status=200)
