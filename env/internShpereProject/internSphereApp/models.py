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
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Student'})
    batch = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    temporary_password = models.CharField(max_length=100)
    profile_completed = models.BooleanField(default=False)


class student_Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': CustomUser.STUDENT})

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



# Company Profile
class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Company'})
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    linkedin_profile = models.URLField()
    approved = models.BooleanField(default=False)

# Department Profile
class Department(models.Model):

    DEPARTMENT_CHOICES = [
        (ACCOUNTING, 'Accounting'),
        (COMPUTER_SCIENCE, 'Computer Science'),
        (MANAGEMENT, 'Management'),
        (MARKETING, 'Marketing'),
        (THM, 'THM'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='department_profile', limit_choices_to={'user_type': 'Department'})
    department_choices = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)


class Supervisor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Supervisor'}, related_name='supervisor_profile')
    supervisor_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.supervisor_name
    
# Internship and Career Office
class InternshipCareerOffice(models.Model):
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
    ACCOUNTING = 'Accounting'
    COMPUTER_SCIENCE = 'Computer Science'
    MANAGEMENT = 'Management'
    MARKETING = 'Marketing'
    THM = 'THM'

    DEPARTMENT_CHOICES = [
        (ACCOUNTING, 'Accounting'),
        (COMPUTER_SCIENCE, 'Computer Science'),
        (MANAGEMENT, 'Management'),
        (MARKETING, 'Marketing'),
        (THM, 'THM'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Student'})
    id_number = models.CharField(max_length=100)
    section = models.CharField(max_length=50)
    report_number = models.IntegerField()
    week_start = models.DateField()
    week_end = models.DateField()
    total_hours_completed = models.IntegerField()
    department_choices = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
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
        return f"Report {self.report_number} by {self.user.username}"




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

