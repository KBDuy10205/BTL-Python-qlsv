import io
import pandas as pd
from django.db import transaction
from .models import Score

COLUMNS = {
    "student_code": ["Student Code","MSSV","student_code","code_sv","Mã sinh viên"],
    "full_name":    ["Full Name","Họ và tên","full_name","name"],
    "course_name":  ["Course Name","Tên học phần","course_name","Môn học"],
    "attendance":   ["Attendance","Chuyên cần","cc","diem cc","diemchuyencan"],
    "midterm":      ["Midterm","Giữa kỳ","gk","mid"],
    "final":        ["Final","Cuối kỳ","ck","final"],
}

def _match_col(cols, keys):
    low = [c.lower().strip() for c in cols]
    for k in keys:
        k = k.lower()
        if k in low:
            return cols[low.index(k)]
    return None

@transaction.atomic
def import_scores_from_excel(file_obj):
    df = pd.read_excel(file_obj)
    cols = list(df.columns)
    m = {k: _match_col(cols, v) for k, v in COLUMNS.items()}
    required = ["student_code", "course_name"]
    if any(m[r] is None for r in required):
        raise ValueError("Thiếu cột bắt buộc: Mã sinh viên (student_code) và Tên học phần (course_name)")

    created, updated = 0, 0
    for _, row in df.iterrows():
        scode = str(row[m["student_code"]]).strip()
        fname = str(row[m["full_name"]]).strip() if m["full_name"] else ""
        cname = str(row[m["course_name"]]).strip()

        att = float(row[m["attendance"]]) if m["attendance"] else 0
        mid = float(row[m["midterm"]])    if m["midterm"]    else 0
        fin = float(row[m["final"]])      if m["final"]      else 0

        obj, is_created = Score.objects.update_or_create(
            StudentCode=scode, CourseName=cname,
            defaults={"FullName": fname, "Attendance": att, "Midterm": mid, "Final": fin}
        )
        created += 1 if is_created else 0
        updated += 0 if is_created else 1
    return {"created": created, "updated": updated}

def export_scores_to_excel(queryset):
    data = []
    for s in queryset:
        data.append({
            "Mã sinh viên": s.StudentCode,
            "Họ và tên": s.FullName,
            "Tên học phần": s.CourseName,
            "Chuyên cần (10%)": s.Attendance,
            "Giữa kỳ (20%)": s.Midterm,
            "Cuối kỳ (70%)": s.Final,
            "Tổng kết": s.Total,
        })
    df = pd.DataFrame(data)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Scores")
    buffer.seek(0)
    return buffer
