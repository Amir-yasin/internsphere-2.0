from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import * 
from django.contrib.auth.models import User
from .forms import *


# Create your views here.
# main pages views
def home(request):
    return render(request, 'main_pages/index.html', {'current_page': 'home'})
def about(request):
    return render(request, 'main_pages/About.html', {'current_page': 'about'})
def contact(request):
    return render(request, 'main_pages/contact.html', {'current_page': 'contact'})





# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # Save the user but don't commit yet
#             user.user_type = form.cleaned_data.get('user_type')  # Get the user_type from the form
#             user.save()  # Now save the user with the user_type
#             messages.success(request, 'Account created successfully. You can now log in.')
#             return redirect('login')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = UserRegistrationForm()
    
#     return render(request, 'main_pages/register.html', {'form': form})



def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main_pages/register.html', {'form': form})

def student_profile(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            student_profile = form.save(commit=False)
            student_profile.user = request.user
            student_profile.save()
            return redirect('student_pages/student_dashboard')
    else:
        form = StudentProfileForm()
    return render(request, 'create_student_profile.html', {'form': form})

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
    return render(request, 'company_profile.html', {'form': form})






def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user.user_type == CustomUser.STUDENT:
                return redirect('student_profile')
            elif user.user_type == CustomUser.COMPANY:
                return redirect('company_profile')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'main_pages/login.html')

    return render(request, 'main_pages/login.html')


def logout(request):
    auth_logout(request)
    return redirect('login')
# def services(request):
#     return render(request, 'main_pages/services.html', {'current_page': 'services'})



# student pages views

def Graduate_students(request):
    return render(request, 'student_pages/Graduate_students.html', {'current_page': 'Graduate_students'})
def intern_opportunities(request):
    return render(request, 'student_pages/intern_opportunities.html', {'current_page': 'intern_opportunities'})
def Internships(request):
    return render(request, 'student_pages/Internships.html', {'current_page': 'Internships'})
def student_profile(request):
    return render(request, 'student_pages/student_profile.html', {'current_page': 'student_profile'})
def bi_weekly_report(request):
    return render(request, 'student_pages/bi_weekly_report.html', {'current_page': 'bi_weekly_report'})

# @login_required
def student_dashboard(request):
    return render(request, 'student_pages/student_dashboard.html', {'current_page': 'student_dashboard'})
def applications(request):
    return render(request, 'student_pages/applications.html', {'current_page': 'applications'})
def stud_notification(request):
    return render(request, 'student_pages/stud_notification.html', {'current_page': 'stud_notification'})



# company pages views

def post_internship(request):
    return render(request, 'company_pages/post_internship.html', {'current_page': 'post_internship'})
def company_profile(request):
    return render(request, 'company_pages/company_profile.html', {'current_page': 'company_profile'})
def company_dashboard(request):
    return render(request, 'company_pages/company_dashboard.html', {'current_page': 'company_dashboard'})
def view_applicants(request):
    return render(request, 'company_pages/view_applicants.html', {'current_page': 'view_applicants'})
def attendance(request):
    return render(request, 'company_pages/attendance.html', {'current_page': 'attendance'})
def accepted_interns(request):
    return render(request, 'company_pages/accepted_interns.html', {'current_page': 'accepted_interns'})
def evaluate_intern(request):
    return render(request, 'company_pages/evaluate_intern.html', {'current_page': 'evaluate_intern'})

