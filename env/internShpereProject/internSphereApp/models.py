from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Student', 'Student'),
        ('Company', 'Company'),
        ('Department', 'Department'),
        ('Supervisor', 'Supervisor'),
        ('Admin', 'Admin'),
        ('InternshipCareerOffice', 'Internship & Career Office'),
    )
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)

# Student Profile
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Student'})
    batch = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    temporary_password = models.CharField(max_length=100)
    profile_completed = models.BooleanField(default=False)

# Company Profile
class CompanyProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Company'})
    company_name = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)

# Department Profile
class DepartmentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Department'})

# Supervisor Profile
class SupervisorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Supervisor'})

# Internship and Career Office
class InternshipCareerOfficeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'InternshipCareerOffice'})

# Internship Posting
class InternshipPosting(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirement = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    posted_on = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, default='Open')  # Open or Closed
        
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
# class BiWeeklyReport(models.Model):
#     student = models.ForeignKey(student_Profile, on_delete=models.CASCADE)
#     report_period_start = models.DateField()
#     report_period_end = models.DateField()
#     report_content = models.TextField()
#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.student.full_name} - {self.report_period_start} to {self.report_period_end}"
# Bi-Weekly Report
class BiWeeklyReport(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    report_number = models.IntegerField()
    content = models.TextField()

# Other relevant models (Final Reports, Evaluation, Attendance, etc.) follow similar structure.


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

