from django.db import models
from django.conf import settings
# class Student(models.Model):
#     student_id = models.AutoField(primary_key=True, db_column="StudentID")
#     full_name = models.CharField(max_length=100, db_column="FullName")
#     # account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='student_profile', db_column="AccountID")
#     account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
#     gender = models.CharField(max_length=10, db_column="Gender")
#     birth_date = models.DateField(db_column="BirthDate")
#     address = models.CharField(max_length=255, db_column="Address")
#     phone_number = models.CharField(max_length=15, db_column="Phone")
#     addmission_year = models.IntegerField(db_column="AdmissionYear")
#     email = models.EmailField(db_column="Email")

#     class Meta:
#         db_table = "Students"


# class Faculty(models.Model):
#     faculty_id = models.AutoField(primary_key=True, db_column="FacultyID")
#     faculty_name = models.CharField(max_length=100, db_column="FacultyName")
#     office = models.CharField(max_length=100, db_column="Office")
#     phone = models.CharField(max_length=15, db_column="Phone")

#     class Meta:
#         db_table = "Faculties"

class Major(models.Model):
    major_id = models.AutoField(primary_key=True, db_column="MajorID")
    major_name = models.CharField(max_length=100, db_column="MajorName")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, db_column="FacultyID")

    class Meta:
        db_table = "Majors"


class Course(models.Model):
    course_id = models.AutoField(primary_key=True, db_column="CourseID")
    course_name = models.CharField(max_length=100, db_column="CourseName")
    credit = models.IntegerField(db_column="Credit")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, db_column="FacultyID")

    class Meta:
        db_table = "Courses"


class MajorCourse(models.Model):
    major = models.ForeignKey(Major, on_delete=models.CASCADE, db_column="MajorID")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column="CourseID")
    is_required = models.BooleanField(db_column="IsRequired")

    class Meta:
        db_table = "Major_Course"
        unique_together = (("major", "course"),)


class Lecturer(models.Model):
    lecturer_id = models.AutoField(primary_key=True, db_column="LecturerID")
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="AccountID")
    full_name = models.CharField(max_length=100, db_column="FullName")
    email = models.EmailField(db_column="Email")
    phone = models.CharField(max_length=15, db_column="Phone")
    office = models.CharField(max_length=100, db_column="Office")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, db_column="FacultyID")

    class Meta:
        db_table = "Lecturers"


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True, db_column="ScheduleID")
    day_of_week = models.CharField(max_length=15, db_column="DayOfWeek")
    start_period = models.IntegerField(db_column="StartPeriod")
    period_count = models.IntegerField(db_column="PeriodCount")
    start_date = models.DateField(db_column="StartDate")
    end_date = models.DateField(db_column="EndDate")
    room = models.CharField(max_length=100, db_column="Room")

    class Meta:
        db_table = "Schedule"


class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True, db_column="SemesterID")
    year = models.IntegerField(db_column="Year")
    term = models.CharField(max_length=20, db_column="Term")
    credit_fee = models.DecimalField(max_digits=12, decimal_places=2, db_column="CreditFee")
    start_date = models.DateField(db_column="StartDate")
    end_date = models.DateField(db_column="EndDate")

    class Meta:
        db_table = "Semesters"

class Class(models.Model):
    class_id = models.AutoField(primary_key=True, db_column="ClassID")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column="CourseID")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, db_column="SemesterID")
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, db_column="LecturerID")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, db_column="ScheduleID")
    class_name = models.CharField(max_length=100, db_column="ClassName")
    capacity = models.IntegerField(db_column="Capacity")

    class Meta:
        db_table = "Classes"





class StudentPayment(models.Model):
    payment_id = models.AutoField(primary_key=True, db_column="PaymentID")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column="StudentID")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, db_column="SemesterID")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, db_column="TotalAmount")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, db_column="PaidAmount")
    status = models.CharField(max_length=20, db_column="Status")
    due_date = models.DateField(db_column="DueDate")
    paid_date = models.DateField(null=True, blank=True, db_column="PaidDate")

    class Meta:
        db_table = "StudentPayments"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column="StudentID")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, db_column="ClassID")
    midterm_grade = models.DecimalField(max_digits=4, decimal_places=2, db_column="MidtermGrade", null=True, blank=True)
    final_grade = models.DecimalField(max_digits=4, decimal_places=2, db_column="FinalGrade", null=True, blank=True)
    status = models.CharField(max_length=20, db_column="Status")  # 'Passed', 'Failed', 'InProgress'
    enrollment_date = models.DateField(db_column="EnrollmentDate")

    class Meta:
        db_table = "Enrollments"
        unique_together = (("student", "class_obj"),)














