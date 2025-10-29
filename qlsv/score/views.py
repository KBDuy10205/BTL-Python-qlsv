from django.db.models import Avg, F, ExpressionWrapper, FloatField, Count, Max, Min
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from rest_framework import viewsets, permissions, decorators, response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Score
from .serializers import ScoreSerializer, ManualScoreEditSerializer
from .utils_excel import import_scores_from_excel, export_scores_to_excel as build_excel_buffer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all().order_by("StudentCode", "CourseName")
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated]  # test nhanh: đổi tạm AllowAny
    filterset_fields = ["StudentCode", "FullName", "CourseName"]
    search_fields = ["StudentCode", "FullName", "CourseName"]
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
        buffer = build_excel_buffer(qs)
        resp = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        resp["Content-Disposition"] = 'attachment; filename="scores.xlsx"'
        return resp

    @decorators.action(detail=False, methods=["get"], url_path="avg_by_student")
    def avg_by_student(self, request):
        scode = request.query_params.get("student_code")
        expr_total = ExpressionWrapper(
            (F("Attendance") * 0.10) + (F("Midterm") * 0.20) + (F("Final") * 0.70),
            output_field=FloatField(),
        )
        qs = Score.objects.all()
        if scode:
            qs = qs.filter(StudentCode=scode)
        data = (
            qs.values("StudentCode", "FullName")
            .annotate(avg_total=Avg(expr_total), total_records=Count("pk"))
            .order_by("StudentCode")
        )
        res = [
            {
                "StudentCode": r["StudentCode"],
                "FullName": r["FullName"],
                "RecordsCount": r["total_records"],
                "AverageTotal": round(float(r["avg_total"] or 0), 2),
            }
            for r in data
        ]
        return response.Response(res, status=200)

    @decorators.action(detail=False, methods=["get"], url_path="chart_data")
    def chart_data(self, request):
        course_name = request.query_params.get("course_name")
        qs = self.get_queryset()
        if course_name:
            qs = qs.filter(CourseName=course_name)
        totals = [s.Total for s in qs]
        if not totals:
            return response.Response({"labels": [], "counts": [], "count": 0, "avg": 0.0}, status=200)
        bins = [0] * 11
        for t in totals:
            i = max(0, min(10, int(round(t))))
            bins[i] += 1
        return response.Response(
            {"labels": [str(i) for i in range(11)], "counts": bins, "count": len(totals),
             "avg": round(sum(totals)/len(totals), 2)},
            status=200,
        )

    @decorators.action(detail=False, methods=["post"], url_path="manual_edit")
    def manual_edit(self, request):
        ser = ManualScoreEditSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        score, _ = Score.objects.get_or_create(
            StudentCode=data["StudentCode"], CourseName=data["CourseName"],
            defaults={"FullName": data.get("FullName", "")},
        )
        for k in ["FullName", "Attendance", "Midterm", "Final"]:
            if k in data and data[k] is not None:
                setattr(score, k, data[k])
        score.save()
        return response.Response(ScoreSerializer(score).data, status=200)

def score_dashboard(request):
    scores = Score.objects.all().order_by("StudentCode", "CourseName")
    if scores.exists():
        avg = round(sum(s.Total for s in scores) / scores.count(), 2)
        if avg >= 9:  rank = "Xuất sắc"
        elif avg >= 8: rank = "Giỏi"
        elif avg >= 6.5: rank = "Khá"
        elif avg >= 5: rank = "Trung bình"
        else:          rank = "Yếu"
    else:
        avg, rank = 0, "Không có dữ liệu"
    return render(request, "score/dashboard.html", {"scores": scores, "avg": avg, "rank": rank})

class ImportScoreView(View):
    def post(self, request, *args, **kwargs):
        upfile = request.FILES.get("file")
        if not upfile:
            return JsonResponse({"detail": "Thiếu file"}, status=400)
        try:
            info = import_scores_from_excel(upfile)
            return JsonResponse({"message": "OK", **info}, status=200)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)

    def get(self, request, *args, **kwargs):
        return render(request, "score/import.html")
    