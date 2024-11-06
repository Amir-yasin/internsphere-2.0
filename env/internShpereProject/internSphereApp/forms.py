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
        model = stud_profile
        fields = ('batch', 'section', 'list_of_students')



class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = stud_profile
        fields = ['email', 'phone_number', 'gender', 'year_of_study', 'skills', 'resume', 'linkedin_profile']     

class CompanyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    company_name = forms.CharField(max_length=255)
    company_address = forms.CharField(max_length=255)
    company_phone = forms.CharField(max_length=15)
    company_description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ('username','email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'Company'

        if commit:
            user.save()
            Company.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_address=self.cleaned_data['company_address'],
                company_phone=self.cleaned_data['company_phone'],
                company_description=self.cleaned_data['company_description']
            )
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class InternshipPostingForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['title', 'description', 'requirement', 'location', 'start_date', 'end_date', 'deadline']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }