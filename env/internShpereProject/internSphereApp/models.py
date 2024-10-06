from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    STUDENT = 'Student'
    COMPANY = 'Company'
    DEPARTMENT = 'Department'
    SUPERVISOR = 'Supervisor'
    ADMIN = 'Admin'
    INTERNSHIP_OFFICE = 'internship_office'
    USER_TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (COMPANY, 'Company'),
        (DEPARTMENT, 'Department'),
        (SUPERVISOR, 'Supervisor'),
        (ADMIN, 'Admin'),
        (INTERNSHIP_OFFICE , 'internship_office'),

    ]
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15)

class student_Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': CustomUser.STUDENT})

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    university = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    year_of_study = models.CharField(max_length=2)
    skills = models.CharField(max_length=1000)
    resume = models.FileField(upload_to='resumes/')
    linkedin_profile = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

class Department(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='department_profile')
    department_name = models.CharField(max_length=100)
    contact_email = models.EmailField()

    def __str__(self):
        return self.department_name

class Supervisor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='supervisor_profile')
    supervisor_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.supervisor_name

class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_profile')

class Internship_Office(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='InternshipOffice_profile')


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
    student = models.ForeignKey(student_Profile, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.internship.title}"


# BiWeeklyReport model for Student
class BiWeeklyReport(models.Model):
    student = models.ForeignKey(student_Profile, on_delete=models.CASCADE)
    report_period_start = models.DateField()
    report_period_end = models.DateField()
    report_content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.report_period_start} to {self.report_period_end}"


# Attendance model for Student
class Attendance(models.Model):
    student = models.ForeignKey(student_Profile, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.status}"


# Evaluation model linking Student and Company
class Evaluation(models.Model):
    student = models.ForeignKey(student_Profile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    comments = models.TextField()
    score = models.IntegerField()
    evaluated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.company.company_name}"

