from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone



# CustomUser
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

    def __str__(self):
        return self.username


# Student Profile
class student_profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Student'})
    batch = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    temporary_password = models.CharField(max_length=100)
    profile_completed = models.BooleanField(default=False)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    year_of_study = models.CharField(max_length=2)
    skills = models.CharField(max_length=1000)
    resume = models.FileField(upload_to='resumes/')
    linkedin_profile = models.URLField(blank=True, null=True)
    list_of_students = models.FileField(upload_to='list_of_students/')

    def __str__(self):
        return self.user.username


# Company Profile
class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Company'})
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_phone = models.CharField(max_length=15)
    company_description = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)  # This field indicates if the company has been approved by the admin
     
    def __str__(self):
        return self.company_name



# Department Profile
class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('Accounting', 'Accounting'),
        ('Computer Science', 'Computer Science'),
        ('Management', 'Management'),
        ('Marketing', 'Marketing'),
        ('THM', 'THM'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='department_profile', limit_choices_to={'user_type': 'Department'})
    department_name = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    department_head = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name


# Supervisor Profile
class Supervisor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Supervisor'}, related_name='supervisor_profile')
    supervisor_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.supervisor_name


# Internship and Career Office
class InternshipCareerOffice(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'InternshipCareerOffice'})
    ICU_director = models.CharField(max_length=100)


# Internship Posting
class Internship(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
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
    student = models.ForeignKey(student_profile, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.internship.title}"


# BiWeeklyReport model
class BiWeeklyReport(models.Model):
    student = models.ForeignKey(student_profile, on_delete=models.CASCADE)
    report_number = models.IntegerField()
    week_start = models.DateField()
    week_end = models.DateField()
    total_hours_completed = models.IntegerField()
    assignment_responsibilities = models.TextField()
    critical_analysis = models.TextField()
    observing_hours = models.IntegerField()
    administrative_hours = models.IntegerField()
    researching_hours = models.IntegerField()
    assisting_hours = models.IntegerField()
    misc_hours = models.IntegerField()
    meetings_discussions = models.TextField()
    course_relevance_suggestions = models.TextField()
    date_submitted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report {self.report_number} by {self.student.user.username}"


# Final Report
class FinalReport(models.Model):
    student = models.ForeignKey(student_profile, on_delete=models.CASCADE)
    report = models.FileField(upload_to='final-reports/')


# Attendance model
class Attendance(models.Model):
    student = models.ForeignKey(student_profile, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"


# Evaluation model linking Student and Company
class Evaluation(models.Model):
    student = models.ForeignKey(student_profile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    feedback = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2)  # out of 100

    def __str__(self):
        return f"Evaluation for {self.student.user.username} by {self.company.company_name}"





#  class Company(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
#     company_name = models.CharField(max_length=100)
#     address = models.CharField(max_length=255)

# class Department(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='department_profile')
#     department_name = models.CharField(max_length=100)
#     contact_email = models.EmailField()

#     def __str__(self):
#         return self.department_name

# class Supervisor(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='supervisor_profile')
#     supervisor_name = models.CharField(max_length=100)
#     contact_email = models.EmailField()
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.supervisor_name



# class Internship_Office(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='InternshipOffice_profile')


# Internship model linked to Company
# class Internship(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     requirement = models.TextField()
#     location = models.CharField(max_length=255)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


# Application model linking Student and Internship
# class Application(models.Model):
#     student = models.ForeignKey(student_Profile, on_delete=models.CASCADE)
#     internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
#     status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
#     applied_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.student.full_name} - {self.internship.title}"


# BiWeeklyReport model for Student




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
# class BiWeeklyReport(models.Model):
#     student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
#     company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
#     report_number = models.IntegerField()
#     content = models.TextField()

# Other relevant models (Final Reports, Evaluation, Attendance, etc.) follow similar structure.


# Attendance model for Student
