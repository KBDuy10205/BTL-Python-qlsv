import io
import pandas as pd
from django.db import transaction
from .models import Student, Course, Score

COLUMNS = {
    "student_code": ["Student Code","MSSV","student_code","code_sv"],
    "student_name": ["Full Name","Họ và tên","Tên học sinh","full_name","name"],
    "course_code":  ["Course Code","Mã HP","course_code","code_hp"],
    "midterm":      ["Midterm","Điểm giữa kỳ","gk","mid"],
    "final":        ["Final","Điểm cuối kỳ","ck","final"],
    "other":        ["Other","Điểm khác","other"]
}

def _match_col(cols, keys):
    low = [c.lower().strip() for c in cols]
    for k in keys:
        if k.lower() in low:
            return cols[low.index(k.lower())]
    return None

@transaction.atomic
def import_scores_from_excel(file_obj):
    df = pd.read_excel(file_obj)
    cols = list(df.columns)
    m = {k: _match_col(cols, v) for k, v in COLUMNS.items()}
    required = ["student_code","student_name","course_code"]
    if any(m[r] is None for r in required):
        raise ValueError("Thiếu cột bắt buộc: student_code, student_name, course_code")

    created, updated = 0, 0
    for _, row in df.iterrows():
        sv_code = str(row[m["student_code"]]).strip()
        sv_name = str(row[m["student_name"]]).strip()
        hp_code = str(row[m["course_code"]]).strip()
        mid = row[m["midterm"]] if m["midterm"] else None
        fin = row[m["final"]]   if m["final"]   else None
        oth = row[m["other"]]   if m["other"]   else None

        student, _ = Student.objects.get_or_create(code=sv_code, defaults={"full_name": sv_name})
        if student.full_name != sv_name and sv_name:
            student.full_name = sv_name; student.save(update_fields=["full_name"])
        course, _ = Course.objects.get_or_create(code=hp_code, defaults={"name": hp_code})

        obj, is_created = Score.objects.update_or_create(
            student=student, course=course,
            defaults={"midterm": mid, "final": fin, "other": oth}
        )
        created += 1 if is_created else 0
        updated += 0 if is_created else 1
    return {"created": created, "updated": updated}

def export_scores_to_excel(queryset):
    data = []
    for s in queryset.select_related("student","course"):
        data.append({
            "Student Code": s.student.code,
            "Full Name": s.student.full_name,
            "Course Code": s.course.code,
            "Course Name": s.course.name,
            "Midterm": s.midterm, "Final": s.final, "Other": s.other, "Total": s.total
        })
    df = pd.DataFrame(data)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Scores")
    buffer.seek(0)
    return buffer
