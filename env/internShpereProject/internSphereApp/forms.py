from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UserTypeForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('company', 'Company'),
        ('department', 'Department'),
        ('supervisor', 'Supervisor'),
        ('internship_office', 'Internship Office')
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'user_type', 'password1', 'password2')



class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = student_Profile
        fields = ['full_name', 'email', 'phone_number', 'gender', 'university', 'major', 'year_of_study', 'skills', 'resume', 'linkedin_profile']
        

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'address']


class DepartmentChoicesForm(forms.Form):
    DEPARTMENT_CHOICES = [
        ('accounting', 'Accounting'),
        ('computer_science', 'Computer Science'),
        ('management', 'Management'),
        ('marketing', 'Marketing'),
        ('thm', 'THM'),
    ]
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)


class BiWeeklyReportForm(forms.ModelForm):
    class Meta:
        model = BiWeeklyReport
        fields = [
            'id_number', 'section', 'report_number', 'week_start', 'week_end', 
            'total_hours_completed', 'department_choices', 'assignment_responsibilities', 
            'critical_analysis', 'observing_hours', 'administrative_hours', 
            'researching_hours', 'assisting_hours', 'misc_hours', 
            'meetings_discussions', 'course_relevance_suggestions'
        ]
        exclude = ['student', 'profile', 'date_submitted'] 

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
