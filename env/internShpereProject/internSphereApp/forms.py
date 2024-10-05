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
        model = Student
        fields = ['phone_number', 'email']

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'address']

# Repeat similar forms for Department, Supervisor, Admin








# class UserRegistrationForm(UserCreationForm):
#     USER_TYPE_CHOICES = [
#         ('student', 'Student'),
#         ('company', 'Company'),
#         ('department', 'Department'),
#         ('supervisor', 'Supervisor'),
#         ('internship_office', 'Internship Office'),
#     ]     
    

#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#     phone_number = forms.CharField(max_length=15, required=True)
#     user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'user_type', 'password1', 'password2']


# # Student profile form
# class StudentProfileForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['full_name', 'email']

# # Company profile form
# class CompanyProfileForm(forms.ModelForm):
#     class Meta:
#         model = Company
#         fields = ['company_name']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
