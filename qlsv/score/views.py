from django.db.models import Avg, F, ExpressionWrapper, FloatField, Count
from django.shortcuts import render
from rest_framework import viewsets, permissions, decorators, response, status
from django_filters.rest_framework import DjangoFilterBackend

from .models import Score
from .serializers import ScoreSerializer, ManualScoreEditSerializer


db_total_expression = ExpressionWrapper(
    (F("Attendance") * F("WeightAttendance")) +
    (F("Midterm") * F("WeightMidterm")) +
    (F("Final") * F("WeightFinal")),
    output_field=FloatField(),
)


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all().order_by("StudentCode", "CourseId")
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["StudentCode", "CourseId"]
    search_fields = ["StudentCode", "CourseId"]

    @decorators.action(detail=False, methods=["get"], url_path="by_student")
    def by_student(self, request):
        student_code = request.query_params.get("StudentCode")
        if not student_code:
            return response.Response({"detail": "Thiếu mã sinh viên"}, status=400)

        qs = self.get_queryset().filter(StudentCode=student_code)
        serializer = self.get_serializer(qs, many=True)
        return response.Response(serializer.data)

    @decorators.action(detail=False, methods=["get"], url_path="avg_by_student")
    def avg_by_student(self, request):
        scode = request.query_params.get("student_code")
        
        qs = Score.objects.all()
        if scode:
            qs = qs.filter(StudentCode=scode)
        
        data = (
            qs.values("StudentCode")
            .annotate(
                avg_total=Avg(db_total_expression),
                total_records=Count("pk")
            )
            .order_by("StudentCode")
        )
        
        res = [
            {
                "StudentCode": r["StudentCode"],
                "RecordsCount": r["total_records"],
                "AverageTotal": round(float(r["avg_total"] or 0), 2),
            }
            for r in data
        ]
        return response.Response(res, status=200)

    @decorators.action(detail=False, methods=["get"], url_path="chart_data")
    def chart_data(self, request):
        course_id = request.query_params.get("course_id")
        
        qs = self.get_queryset().annotate(total_score=db_total_expression)
        
        if course_id:
            qs = qs.filter(CourseId=course_id)
            
        totals = [s.total_score for s in qs.iterator()]
        
        if not totals:
            return response.Response({"labels": [], "counts": [], "count": 0, "avg": 0.0}, status=200)
        
        bins = [0] * 11
        for t in totals:
            from decimal import Decimal, ROUND_HALF_UP
            score_decimal = Decimal(t or 0)
            i = int(score_decimal.quantize(Decimal('1'), rounding=ROUND_HALF_UP))
            i = max(0, min(10, i))
            bins[i] += 1
            
        return response.Response(
            {
                "labels": [str(i) for i in range(11)],
                "counts": bins,
                "count": len(totals),
                "avg": round(sum(totals) / len(totals), 2),
            },
            status=200,
        )

    @decorators.action(detail=False, methods=["post"], url_path="manual_edit")
    def manual_edit(self, request):
        ser = ManualScoreEditSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        
        score_instance = ser.save()
        
        return response.Response(ScoreSerializer(score_instance).data, status=200)


def score_dashboard(request):
    total_records = Score.objects.count()
    total_students = Score.objects.values("StudentCode").distinct().count()
    
    stats = Score.objects.aggregate(
        avg_gpa=Avg(db_total_expression),
        max_score=Max(db_total_expression),
        min_score=Min(db_total_expression),
    )
    
    context = {
        "total_students": total_students,
        "total_records": total_records,
        "average_gpa": f"{(stats.get('avg_gpa') or 0):.2f}",
        "max_score": f"{(stats.get('max_score') or 0):.2f}" if stats.get("max_score") is not None else "N/A",
        "min_score": f"{(stats.get('min_score') or 0):.2f}" if stats.get("min_score") is not None else "N/A",
        "scores_list": Score.objects.order_by("-pk")[:50],
    }
    return render(request, "score_management/dashboard.html", context)
