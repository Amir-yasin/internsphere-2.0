from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import * 
from django.contrib.auth.models import User
from .forms import *
from django.utils.crypto import get_random_string
import pandas as pd  

# Create your views here.
# main pages views
def home(request):
    return render(request, 'main_pages/index.html', {'current_page': 'home'})
def about(request):
    return render(request, 'main_pages/About.html', {'current_page': 'about'})
def contact(request):
    return render(request, 'main_pages/contact.html', {'current_page': 'contact'})


def register_students(request):
    if request.method == 'POST':
        batch = request.POST['batch']
        section = request.POST['section']
        excel_file = request.FILES['student_list']
        
        # Process Excel file
        df = pd.read_excel(excel_file)
        for index, row in df.iterrows():
            temp_password = get_random_string(length=6)
            user = CustomUser.objects.create_user(
                username=row['username'], 
                password=temp_password, 
                user_type='Student'
            )
            student_profile.objects.create(
                user=user, 
                batch=batch, 
                section=section, 
                temporary_password=temp_password
            )
        return redirect('student_list')
    
    return render(request, 'admin/register_students.html')



def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main_pages/register.html', {'form': form, 'current_page': 'contact'})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user.user_type == CustomUser.STUDENT:
                return redirect('student_dashboard')
            elif user.user_type == CustomUser.COMPANY:
                return redirect('company_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'main_pages/login.html')

    return render(request, 'main_pages/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')


# student pages views
@login_required
def Graduate_students(request):
    return render(request, 'student_pages/Graduate_students.html', {'current_page': 'Graduate_students'})

@login_required
def intern_opportunities(request):
    return render(request, 'student_pages/intern_opportunities.html', {'current_page': 'intern_opportunities'})

@login_required
def Internships(request):
    return render(request, 'student_pages/Internships.html', {'current_page': 'Internships'})

@login_required
def student_profile(request):
    student = request.user.student_profile
    if request.method == 'POST':
        student.email = request.POST['email']
        student.phone_number = request.POST['phone_number']
        student.gender = request.POST['gender']
        student.year_of_study = request.POST['year_of_study']
        student.skills = request.POST['skills']
        student.linkedin_profile = request.POST['linkedin_profile']
        student.resume = request.FILES['resume']
        student.profile_completed = True
        student.save()
        return redirect('dashboard')
    
    return render(request, 'students/student_profile.html', {'student': student})
# def student_profile(request):
#     if request.method == 'POST':
#         form = StudentProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Check if profile already exists for this user
#             try:
#                 student_profile = student_Profile.objects.get(user=request.user)
#                 form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)  # Update existing profile
#                 student_profile = form.save()  # Update existing profile
#                 messages.success(request, 'Profile updated successfully!') 
#             except student_Profile.DoesNotExist:
#                 # Profile does not exist, create a new one
#                 student_profile = form.save(commit=False)
#                 student_profile.user = request.user
#                 student_profile.save()
#                 messages.success(request, 'Profile created successfully!')  # Success message for creation


#             return redirect('student_dashboard')
#     else:
#         form = StudentProfileForm()

#     return render(request, 'student_pages/student_profile.html', {'form': form})

@login_required
def bi_weekly_report(request):
    if request.method == 'POST':
        form = BiWeeklyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.student = request.user.student_Profile
            report.company = CompanyProfile.objects.get(user=request.user.student_Profile.company)
            report.save()
            return redirect('student_dashboard')
    else:
        form = BiWeeklyReportForm()
    return render(request, 'student_pages/bi_weekly_report.html', {'current_page': 'bi_weekly_report'})

@login_required
def student_dashboard(request):
    if request.user.user_type != 'Student':
        return redirect('home')
    return render(request, 'student_pages/student_dashboard.html', {'current_page': 'student_dashboard'})

@login_required
def applications(request):
    return render(request, 'student_pages/applications.html', {'current_page': 'applications'})

@login_required
def stud_notification(request):
    return render(request, 'student_pages/stud_notification.html', {'current_page': 'stud_notification'})



# company pages views

@login_required
def post_internship(request):
    if request.method == 'POST':
        form = InternshipPostingForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.company = request.user.company
            internship.save()
            return redirect('company_dashboard')
    else:
        form = InternshipPostingForm()
    return render(request, 'company_pages/post_internship.html', {'current_page': 'post_internship'})

@login_required
def company_profile(request):
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST)
        if form.is_valid():
            company_profile = form.save(commit=False)
            company_profile.user = request.user
            company_profile.save()
            return redirect('company_pages/company_dashboard')
    else:
        form = CompanyProfileForm()
        return render(request, 'company_pages/company_profile.html', {'form':'form','current_page': 'company_profile'})



@login_required
def company_dashboard(request):
    return render(request, 'company_pages/company_dashboard.html', {'current_page': 'company_dashboard'})

@login_required
def view_applicants(request):
    return render(request, 'company_pages/view_applicants.html', {'current_page': 'view_applicants'})

@login_required
def attendance(request):
    return render(request, 'company_pages/attendance.html', {'current_page': 'attendance'})

@login_required
def accepted_interns(request):
    return render(request, 'company_pages/accepted_interns.html', {'current_page': 'accepted_interns'})

@login_required
def evaluate_intern(request):
    return render(request, 'company_pages/evaluate_intern.html', {'current_page': 'evaluate_intern'})



# Admin Views
@login_required
def admin_dashboard(request):
    if request.user.user_type != 'Admin':
        return redirect('home')
    return render(request, 'admin_dashboard.html')