from rest_framework import viewsets, permissions, decorators, response, status
from django.db.models import Avg
from django.http import HttpResponse
from .models import Student, Course, Score
from .serializers import StudentSerializer, CourseSerializer, ScoreSerializer
from .utils_excel import import_scores_from_excel, export_scores_to_excel

class IsAuth(permissions.IsAuthenticated): pass

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["code","full_name"]
    search_fields = ["code","full_name"]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["code","name"]
    search_fields = ["code","name"]

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related("student","course").all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["student","course"]
    search_fields = ["student__code","student__full_name","course__code","course__name"]

    # POST /api/scores/import_excel/
    @decorators.action(detail=False, methods=["post"], url_path="import_excel")
    def import_excel(self, request):
        f = request.FILES.get("file")
        if not f: return response.Response({"detail":"Thiếu file"}, status=400)
        info = import_scores_from_excel(f)
        return response.Response(info, status=200)

    # GET /api/scores/export_excel/?course=<id>&student=<id>
    @decorators.action(detail=False, methods=["get"], url_path="export_excel")
    def export_excel(self, request):
        qs = self.filter_queryset(self.get_queryset())
        buf = export_scores_to_excel(qs)
        resp = HttpResponse(buf.getvalue(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        resp["Content-Disposition"] = 'attachment; filename="scores.xlsx"'
        return resp

    # GET /api/scores/avg_by_student/?student_id=1
    @decorators.action(detail=False, methods=["get"], url_path="avg_by_student")
    def avg_by_student(self, request):
        sid = request.query_params.get("student_id")
        qs = Score.objects.filter(student_id=sid) if sid else Score.objects.all()
        data = qs.values("student__id","student__code","student__full_name") \
                 .annotate(avg_total=Avg("midterm")*0 + Avg("final")*0)  # placeholder
        # dùng property total không thể annotate trực tiếp; ta tính TB theo (midterm*wm + final*wf + other*wo)
        from django.db.models import F, ExpressionWrapper, FloatField
        qs = Score.objects.filter(student_id=sid) if sid else Score.objects.all()
        expr = ExpressionWrapper(
            (F("midterm")*F("weight_midterm")) + (F("final")*F("weight_final")) + (F("other")*F("weight_other")),
            output_field=FloatField()
        )
        agg = qs.values("student__id","student__code","student__full_name") \
                .annotate(avg_total=Avg(expr)).order_by("student__code")
        return response.Response(list(agg))

    # GET /api/scores/chart_data/?course_id=...
    # trả JSON phân phối điểm (bins 0-10) để frontend vẽ biểu đồ
    @decorators.action(detail=False, methods=["get"], url_path="chart_data")
    def chart_data(self, request):
        course_id = request.query_params.get("course_id")
        qs = self.get_queryset()
        if course_id:
            qs = qs.filter(course_id=course_id)
        totals = [s.total for s in qs]
        bins = [0]*11
        for t in totals:
            i = max(0, min(10, int(round(t))))
            bins[i] += 1
        return response.Response({
            "labels": [str(i) for i in range(0,11)],
            "counts": bins,
            "count": len(totals),
            "avg": round(sum(totals)/len(totals),2) if totals else 0.0
        })
