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

class StudentCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('batch', 'section', 'list_of_students')



class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = student_Profile
        fields = ['email', 'phone_number', 'gender', 'year_of_study', 'skills', 'resume', 'linkedin_profile']
        

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'company_address', 'company_phone', 'company_description']

# Repeat similar forms for Department, Supervisor, Admin


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
