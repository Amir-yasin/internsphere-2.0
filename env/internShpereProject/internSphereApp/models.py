from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
import datetime
from django.utils.timezone import now



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
class stud_profile(models.Model):
    DEPARTMENT_CHOICES = [
        ('Accounting', 'Accounting'),
        ('Computer Science', 'Computer Science'),
        ('Management', 'Management'),
        ('Marketing', 'Marketing'),
        ('THM', 'THM'),
    ]
        
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='stud_profile' , limit_choices_to={'user_type': 'Student'})
    batch = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    temporary_password = models.CharField(max_length=100)
    profile_completed = models.BooleanField(default=False)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    year_of_study = models.CharField(max_length=2)
    skills = models.CharField(max_length=1000)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)  # Ensures matching with sector choices
    resume = models.FileField(upload_to='resumes/')
    linkedin_profile = models.URLField(blank=True, null=True)
    list_of_students = models.FileField(upload_to='list_of_students/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='company', limit_choices_to={'user_type': 'Company'})
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_phone = models.CharField(max_length=15)
    company_description = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)  # Indicates if approved by admin

    def __str__(self):
        return self.company_name


class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('Accounting', 'Accounting'),
        ('Computer Science', 'Computer Science'),
        ('Management', 'Management'),
        ('Marketing', 'Marketing'),
        ('THM', 'THM'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='department_profile',limit_choices_to={'user_type': 'Department'})
    department_name = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    department_head = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.department_name} - {self.department_head}"

    
    
class Supervisor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='supervisor_profile',limit_choices_to={'user_type': 'Supervisor'})
    supervisor_name = models.CharField(max_length=100)
    department = models.ForeignKey('Department',  on_delete=models.SET_NULL,null=True,blank=False,related_name='supervisors')

    def __str__(self):
        return f"{self.supervisor_name} ({self.department.department_name})"
    
    
    
# Internship and Career Office
class InternshipCareerOffice(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'InternshipCareerOffice'})
    ICU_director = models.CharField(max_length=100)


# Internship Posting

def default_deadline():
    return (timezone.now() + datetime.timedelta(days=30)).date()

class Internship(models.Model):
    SECTOR_CHOICES = [
        ('Accounting', 'Accounting'),
        ('Computer Science', 'Computer Science'),
        ('Management', 'Management'),
        ('Marketing', 'Marketing'),
        ('THM', 'THM'),
    ]
    
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirement = models.TextField()
    location = models.CharField(max_length=255)
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES)  
    start_date = models.DateField()
    end_date = models.DateField()
    deadline = models.DateField(null=True, default=default_deadline)
    posted_on = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, default='Open')  # Open or Closed

    def __str__(self):
        return self.title

    def is_expired(self):
        return self.deadline < timezone.now().date()

    def close_if_expired(self):
        if self.is_expired():
            self.status = 'Closed'
            self.save()

# Application model linking Student and Internship
class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey('stud_profile', on_delete=models.CASCADE, related_name='applications')
    internship = models.ForeignKey('Internship', on_delete=models.CASCADE, related_name='applications')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='applications')
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    is_active = models.BooleanField(default=False)  # Indicates the active company

    def __str__(self):
        return f"{self.student.user.username} - {self.internship.title} ({self.status})"
 
    
# BiWeeklyReport model
class BiWeeklyReport(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(stud_profile, on_delete=models.CASCADE, related_name="biweekly_reports")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="biweekly_reports")
    application_status = models.ForeignKey(Application, on_delete=models.CASCADE)
    report_number = models.PositiveIntegerField()
    week_start = models.DateField()
    week_end = models.DateField()
    total_hours_completed = models.PositiveIntegerField()
    assignment_responsibilities = models.TextField()
    critical_analysis = models.TextField()
    observing_hours = models.PositiveIntegerField()
    administrative_hours = models.PositiveIntegerField()
    researching_hours = models.PositiveIntegerField()
    assisting_hours = models.PositiveIntegerField()
    misc_hours = models.PositiveIntegerField()
    meetings_discussions = models.TextField()
    course_relevance_suggestions = models.TextField()
    date_submitted = models.DateTimeField(default=now)

    company_approval_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending'
    )
    company_approval_date = models.DateTimeField(null=True, blank=True)
    internship_office_approval_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending'
    )
    internship_office_approval_date = models.DateTimeField(null=True, blank=True)
    department_approval_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending'
    )
    department_approval_date = models.DateTimeField(null=True, blank=True)
    supervisor_approval_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending'
    )
    supervisor_approval_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report {self.report_number} by {self.student.user.username}"


# Final Report
class FinalReport(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.OneToOneField(
        stud_profile, on_delete=models.CASCADE, related_name='final_report'
    )
    report_file = models.FileField(upload_to='final_reports/')
    submitted_at = models.DateTimeField(null=True, blank=True)

    company_approval_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending'
    )
    company_approval_date = models.DateTimeField(null=True, blank=True)
    internship_office_approval_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending'
    )
    internship_office_approval_date = models.DateTimeField(null=True, blank=True)
    department_approval_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending'
    )
    department_approval_date = models.DateTimeField(null=True, blank=True)
    supervisor_approval_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending'
    )
    supervisor_approval_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Final Report by {self.student.user.username}"



# Attendance model
class Attendance(models.Model):
    student = models.ForeignKey(stud_profile, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"


# Evaluation model linking Student and Company


from django.conf import settings

class Evaluation(models.Model):
    student = models.ForeignKey(
        stud_profile, on_delete=models.CASCADE, related_name="student_evaluations"
    )
    company = models.ForeignKey(
        'Company', on_delete=models.CASCADE, related_name="company_evaluations"
    )
    content = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    icu_approval_status = models.CharField(
        max_length=10, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending"
    )
    icu_approval_date = models.DateTimeField(null=True, blank=True)
    department_approval_status = models.CharField(
        max_length=10, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending"
    )
    department_approval_date = models.DateTimeField(null=True, blank=True)
    supervisor_approval_status = models.CharField(
        max_length=10, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending"
    )
    supervisor_approval_date = models.DateTimeField(null=True, blank=True)
    assigned_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supervisor_evaluations"
    )

    def __str__(self):
        return f"Evaluation for {self.student.get_full_name()}"
