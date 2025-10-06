from django.db import models

class Major(models.Model):
    major_id = models.AutoField(primary_key=True, db_column='MajorID')
    major_name = models.CharField(max_length=100, db_column='MajorName')
    faculty_name = models.CharField(max_length=100, db_column='FacultyName', null=True, blank=True)

    class Meta:
        db_table = 'Majors'

    def __str__(self):
        return self.major_name
