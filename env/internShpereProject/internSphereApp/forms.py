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
        fields = ['email', 'phone_number', 'gender', 'department', 'year_of_study', 'skills', 'resume', 'linkedin_profile']     



class BiWeeklyReportForm(forms.ModelForm):
    class Meta:
        model = BiWeeklyReport
        fields = [
            'report_number',
            'week_start',
            'week_end',
            'total_hours_completed',
            'assignment_responsibilities',
            'critical_analysis',
            'observing_hours',
            'administrative_hours',
            'researching_hours',
            'assisting_hours',
            'misc_hours',
            'meetings_discussions',
            'course_relevance_suggestions'
        ]
        widgets = {
            'week_start': forms.DateInput(attrs={'type': 'date'}),
            'week_end': forms.DateInput(attrs={'type': 'date'}),
        }

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
        fields = ['title', 'description', 'requirement', 'location','sector', 'start_date', 'end_date', 'deadline']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
        


class InternshipCareerOfficeForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = InternshipCareerOffice
        fields = ['ICU_director']

    def save(self, commit=True):
        user = CustomUser(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            user_type='InternshipCareerOffice'
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            career_office = super().save(commit=False)
            career_office.user = user
            career_office.save()
        return career_office



class DepartmentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    department_name = forms.ChoiceField(choices=Department.DEPARTMENT_CHOICES, required=True)
    department_head = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def save(self, commit=True):
        # Save CustomUser data
        user = CustomUser(
            username=self.cleaned_data['username'],  # Username provided by admin
            user_type='Department'
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        # Save Department data
        department = Department(
            user=user,
            department_name=self.cleaned_data['department_name'],
            department_head=self.cleaned_data['department_head']
        )
        department.save()

        return user

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['supervisor_name', 'department']