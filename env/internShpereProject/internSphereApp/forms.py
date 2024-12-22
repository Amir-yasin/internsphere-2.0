from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import get_user_model
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


CustomUser = get_user_model()

class SupervisorRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text="Username for the supervisor"
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        help_text="Password for the supervisor"
    )

    class Meta:
        model = Supervisor
        fields = ['supervisor_name', 'department']

    def save(self, commit=True):
        supervisor = super().save(commit=False)

        # Create or update the user instance for the supervisor
        user_data = {
            'username': self.cleaned_data['username'],
        }
        if commit:
            user = CustomUser.objects.create_user(
                **user_data,
                password=self.cleaned_data['password'],
                user_type='Supervisor'
            )
            supervisor.user = user
            supervisor.save()
        return supervisor
    
    
class FinalReportForm(forms.ModelForm):
    class Meta:
        model = FinalReport
        fields = ['report_file']
        widgets = {
            'report_file': forms.ClearableFileInput(attrs={'accept': '.pdf'}),
        }
        

class BiweeklyReportApprovalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
        if fields:
            # Collect fields to remove
            fields_to_remove = [field_name for field_name in self.fields if field_name not in fields]
            # Remove fields after iteration
            for field_name in fields_to_remove:
                self.fields.pop(field_name)

    class Meta:
        model = BiWeeklyReport
        fields = [
            "company_approval_status",
            "internship_office_approval_status",
            "department_approval_status",
            "supervisor_approval_status",
        ]
class FinalReportApprovalForm(forms.ModelForm):
    class Meta:
        model = FinalReport
        fields = [
            "company_approval_status",
            "internship_office_approval_status",
            "department_approval_status",
            "supervisor_approval_status",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.company_approval_status == "Approved" and not instance.company_approval_date:
            instance.company_approval_date = now()
        if instance.internship_office_approval_status == "Approved" and not instance.internship_office_approval_date:
            instance.internship_office_approval_date = now()
        if instance.department_approval_status == "Approved" and not instance.department_approval_date:
            instance.department_approval_date = now()
        if instance.supervisor_approval_status == "Approved" and not instance.supervisor_approval_date:
            instance.supervisor_approval_date = now()
        if commit:
            instance.save()
        return instance
from django import forms

# class EvaluationForm(forms.Form):
#     question_1 = forms.ChoiceField(
#         label="Demonstrates the ability to complete assigned tasks on time",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_2 = forms.ChoiceField(
#         label="Produces work that meets or exceeds quality standards",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_3 = forms.ChoiceField(
#         label="Shows initiative in taking on additional responsibilities",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_4 = forms.ChoiceField(
#         label="Effectively manages time and priorities",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_5 = forms.ChoiceField(
#         label="Follows instructions and procedures accurately",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_6 = forms.ChoiceField(
#         label="Demonstrates competence in using tools and software relevant to the internship",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_7 = forms.ChoiceField(
#         label="Learns and applies new technical skills effectively",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_8 = forms.ChoiceField(
#         label="Solves technical problems independently or with minimal assistance",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_9 = forms.ChoiceField(
#         label="Contributes innovative ideas or solutions to technical challenges",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_10 = forms.ChoiceField(
#         label="Communicates clearly and effectively with team members and supervisors",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_11 = forms.ChoiceField(
#         label="Responds promptly and appropriately to emails and messages",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_12 = forms.ChoiceField(
#         label="Provides clear and concise written reports or documentation",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_13 = forms.ChoiceField(
#         label="Cooperates and collaborates effectively with others",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_14 = forms.ChoiceField(
#         label="Demonstrates respect and professionalism in team settings",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_15 = forms.ChoiceField(
#         label="Supports and assists colleagues when needed",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_16 = forms.ChoiceField(
#         label="Adapts to new tasks, challenges, or work environments with ease",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_17 = forms.ChoiceField(
#         label="Accepts feedback and makes necessary improvements",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_18 = forms.ChoiceField(
#         label="Remains calm and composed under pressure",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_19 = forms.ChoiceField(
#         label="Analyzes problems and identifies appropriate solutions",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_20 = forms.ChoiceField(
#         label="Thinks creatively to overcome challenges or obstacles",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_21 = forms.ChoiceField(
#         label="Makes sound decisions based on available information",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_22 = forms.ChoiceField(
#         label="Maintains a positive and professional attitude throughout the internship",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     question_23 = forms.ChoiceField(
#         label="Demonstrates punctuality and reliable attendance",
#         choices=[(i, str(i)) for i in range(1, 6)],
#         widget=forms.RadioSelect,
#         required=True
#     )

# class EvaluationForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         questions = kwargs.pop('questions', [])
#         super().__init__(*args, **kwargs)

#         for question in questions:
#             self.fields[f'question_{question.id}'] = forms.ChoiceField(
#                 label=question.text,
#                 choices=[(i, str(i)) for i in range(1, 6)],
#                 widget=forms.RadioSelect,
#                 required=True,
#             )
            
class EvaluationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically create fields based on evaluation questions
        questions = EvaluationQuestion.objects.all()
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=[
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5'),
                ],
                widget=forms.RadioSelect(
                    attrs={'class': 'form-check-input'}
                ),
            )