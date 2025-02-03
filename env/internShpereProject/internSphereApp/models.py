from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
import datetime
from django.utils.timezone import now
from django.contrib.auth import get_user_model



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
        
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, 
                                related_name='stud_profile' , limit_choices_to={'user_type': 'Student'})
    batch = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    temporary_password = models.CharField(max_length=100)
    profile_completed = models.BooleanField(default=False)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    year_of_study = models.CharField(max_length=2)
    skills = models.CharField(max_length=1000)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)  
    resume = models.FileField(upload_to='resumes/')
    linkedin_profile = models.URLField(blank=True, null=True)
    list_of_students = models.FileField(upload_to='list_of_students/', blank=True, null=True)


    def get_active_company(self):
        try:
            active_application = self.applications.filter(is_active=True).first()
            if active_application:
                return active_application.company
            return None  # Return None if no active company is found
        except Application.DoesNotExist:
            return None


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
    
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='internships')
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


# Take attendance
class Attendance(models.Model):
    student = models.ForeignKey(stud_profile, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'date')  

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {'Present' if self.present else 'Absent'}"

#Evaluation
class Evaluation(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    student = models.ForeignKey('stud_profile', on_delete=models.CASCADE, related_name='company_evaluations')
    internship = models.ForeignKey('Internship', on_delete=models.CASCADE, related_name='company_evaluations')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='company_evaluations')
    submitted_at = models.DateTimeField(default=now)
    total_score = models.FloatField(default=0)  
    internship_office_approval_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending'
    )
    internship_office_approval_date = models.DateTimeField(null=True, blank=True)
    department_approval_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending'
    )
    department_approval_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Evaluation for {self.student.user.get_full_name()} by {self.company.company_name}"

    def calculate_total_score(self):
        total_raw_score = sum(answer.answer for answer in self.answers.all())
        num_questions = 23  # Fixed number of questions

        if num_questions > 0:  # Avoid division by zero
            calculated_score = (total_raw_score / num_questions) * 10
        else:
            calculated_score = 0

        self.total_score = round(calculated_score, 2)  # Round for clarity
        self.save()


class EvaluationQuestion(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class EvaluationAnswer(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(EvaluationQuestion, on_delete=models.CASCADE)
    answer = models.IntegerField()

    def __str__(self):
        return f"{self.question.text}: {self.answer}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.evaluation.calculate_total_score()
    
    
class SupervisorAssignment(models.Model):
    student = models.ForeignKey('stud_profile', on_delete=models.CASCADE, related_name='supervisor_assignment')
    supervisor = models.ForeignKey('Supervisor', on_delete=models.CASCADE, related_name='supervised_students')
    assigned_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} assigned to {self.supervisor.supervisor_name}"



class SupervisorEvaluation(models.Model):
    student = models.ForeignKey(stud_profile, on_delete=models.CASCADE, related_name="evaluations")
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, related_name="evaluations")

    bi_weekly_report_score = models.IntegerField(default=0)
    final_report_score = models.IntegerField(default=0)
    presentation_score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0, editable=False)  # Auto-calculated

    def save(self, *args, **kwargs):
        # Ensure we fetch the latest company evaluation score
        company_evaluation = Evaluation.objects.filter(student=self.student).order_by('-submitted_at').first()
        company_score = company_evaluation.total_score if company_evaluation else 0

        # Reset total_score before calculating new values
        self.total_score = (
            self.bi_weekly_report_score +
            self.final_report_score +
            self.presentation_score +
            company_score
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Evaluation for {self.student.user.username} by {self.supervisor.supervisor_name}"
