

from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255)


class Department(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='department_profile')
    department_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department_name


# Supervisor model linked to User and Department
class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisor_profile')
    supervisor_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.supervisor_name


# Internship model linked to Company
class Internship(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirement = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Application model linking Student and Internship
class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.internship.title}"


# BiWeeklyReport model for Student
class BiWeeklyReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report_period_start = models.DateField()
    report_period_end = models.DateField()
    report_content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.report_period_start} to {self.report_period_end}"


# Attendance model for Student
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.status}"


# Evaluation model linking Student and Company
class Evaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    comments = models.TextField()
    score = models.IntegerField()
    evaluated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.company.company_name}"

