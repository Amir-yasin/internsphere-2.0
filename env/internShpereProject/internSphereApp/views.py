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
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.shortcuts import get_list_or_404


# main pages views
def home(request):
    return render(request, 'main_pages/index.html', {'current_page': 'home'})
def about(request):
    return render(request, 'main_pages/About.html', {'current_page': 'about'})
def contact(request):
    return render(request, 'main_pages/contact.html', {'current_page': 'contact'})

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
            if user.user_type == 'Student':
                return redirect('student_dashboard')
            elif user.user_type == 'Company':
                return redirect('company_dashboard')
            elif user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('homes')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'main_pages/login.html')

    return render(request, 'main_pages/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')





#admin pages
def register_students(request):
    if request.method == 'POST':
        batch = request.POST['batch']
        section = request.POST['section']
        excel_file = request.FILES['student_list']
        
        # Process Excel file
        df = pd.read_excel(excel_file)
        for index, row in df.iterrows():
            temp_password = row['temporary_password']
            user = CustomUser.objects.create_user(
                username=row['id_number'], 
                first_name=row['first_name'], 
                last_name=row['last_name'], 
                password=temp_password, 
                user_type='Student'
            )
            stud_profile.objects.create(
                user=user, 
                batch=batch, 
                section=section, 
                temporary_password=temp_password
            )
        return redirect('student_list')
    
    return render(request, 'admin_pages/register_students.html')


def student_list(request):
    students = stud_profile.objects.all()
    return render(request, 'admin_pages/student_list.html', {'students': students})

def delete_student(request, student_id):
    student = get_object_or_404(stud_profile, id=student_id)
    student.user.delete()  
    return redirect('student_list')

@login_required
def approve_companies(request):
    pending_companies = Company.objects.filter(approved=False)
    approved_companies = Company.objects.filter(approved=True)
    return render(request, 'admin_pages/approve_companies.html', {'pending_companies': pending_companies, 'approved_companies': approved_companies})

@login_required
def approve_company(request, company_id):
    if request.user.is_superuser: 
        company = get_object_or_404(Company, id=company_id)
        company.approved = True
        company.save()
        messages.success(request, f"{company.company_name} has been approved.")
    return redirect('approve_companies')

@login_required
def view_company_info(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    return render(request, 'admin_pages/view_company_info.html', {'company': company})

@login_required
def delete_company(request, company_id):
    company = get_object_or_404(company, id=company_id)
    company.user.delete()  
    return redirect('approve_companies')





# student pages views
@login_required
def Graduate_students(request):
    return render(request, 'student_pages/Graduate_students.html', {'current_page': 'Graduate_students'})

@login_required
def Internships(request):
    return render(request, 'student_pages/Internships.html', {'current_page': 'Internships'})

@login_required
def student_profile(request):
    student = request.user.stud_profile
    
    if request.method == 'POST':
        # Update student fields with the submitted form data
        student.email = request.POST['email']
        student.phone_number = request.POST['phone_number']
        student.gender = request.POST['gender']
        student.year_of_study = request.POST['year_of_study']
        student.skills = request.POST['skills']
        student.linkedin_profile = request.POST['linkedin_profile']
        student.resume = request.FILES.get('resume')
        student.department = request.POST['department']  # New field
        student.profile_completed = True
        student.save()
        
        messages.success(request, 'Profile created successfully!')
        return redirect('student_dashboard')
    
    return render(request, 'student_pages/student_profile.html', {
        'student': student,
        'department_choices': stud_profile.DEPARTMENT_CHOICES  # Passing choices to template
    })
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
def apply_to_internship(request, internship_id):
    student_profile = request.user.stud_profile
    internship = get_object_or_404(Internship, id=internship_id)

    # Ensure one application per internship
    if Application.objects.filter(student=student_profile, internship=internship).exists():
        messages.error(request, 'You have already applied for this internship.')
        return redirect('intern_opportunities')

    # Create a new application
    Application.objects.create(
        student=student_profile,
        internship=internship,
        company=internship.company,
        status='Pending'
    )
    messages.success(request, 'Your application was submitted successfully!')
    return redirect('intern_opportunities')

@login_required
def applications(request):
    student_profile = request.user.stud_profile
    applications = Application.objects.filter(student=student_profile).select_related('internship', 'company')
    context = {
        'applications': applications,
        'current_page': 'applications'
    }
    return render(request, 'student_pages/applications.html', context)

@login_required
def stud_notification(request):
    return render(request, 'student_pages/stud_notification.html', {'current_page': 'stud_notification'})

@login_required
def view_profile(request, user_id):
    # Retrieve the student user and profile using the correct model names
    student_user = get_object_or_404(CustomUser, id=user_id, user_type='Student')
    student_profile = get_object_or_404(stud_profile, user=student_user)  # Use stud_profile with lowercase 's'

    context = {
        'student_user': student_user,
        'student_profile': student_profile,
        'current_page': 'view_profile'
    }
    
    return render(request, 'student_pages/view_profile.html', context)

@login_required
def intern_opportunities(request):
    try:
        student_profile = stud_profile.objects.get(user=request.user)
        if not student_profile.profile_completed:
            return redirect('student_profile')
        internships = Internship.objects.filter(sector=student_profile.department, status='Open')
        context = {
            'internships': internships,
            'current_page': 'intern_opportunities'
        }
        return render(request, 'student_pages/intern_opportunities.html', context)
    except stud_profile.DoesNotExist:
        return redirect('student_profile')

# # views.py
# import json
# from django.http import JsonResponse
# from .models import Internship

# def internships_by_department(request):
#     # Assume student's department is passed as a query parameter
#     department = request.GET.get('department', None)
#     if department:
#         internships = Internship.objects.filter(sector=department)
#         internships_data = [
#             {
#                 'title': internship.title,
#                 'description': internship.description,
#                 'location': internship.location,
#                 'start_date': internship.start_date,
#                 'end_date': internship.end_date,
#             }
#             for internship in internships
#         ]
#         return JsonResponse({'internships': internships_data})
#     return JsonResponse({'error': 'Department not specified'}, status=400)



# company pages views
def company_register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'Company'
            user.save()
            # Save company profile with approved=False by default
            Company.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                company_address=form.cleaned_data['company_address'],
                company_phone=form.cleaned_data['company_phone'],
                company_description=form.cleaned_data['company_description'],
                approved=False
            )
            return redirect('login')
    else:
        form = CompanyRegistrationForm()

    return render(request, 'company_pages/company_register.html', {'form': form, 'current_page': 'company_register'})

@login_required
def view_company_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id, user_type='Company')
    company = get_object_or_404(Company, user=user)  

    context = {
        'company': company,
        'current_page': 'view_company'
    }
    return render(request, 'company_pages/view_company_profile.html', context)


@login_required
def company_dashboard(request):
    return render(request, 'company_pages/company_dashboard.html', {'current_page': 'company_dashboard', 'internship': internship})


@login_required
def post_internship(request):
    try:
        company = request.user.company
    except Company.DoesNotExist:
        messages.error(request, "You need a company profile to post internships.")
        return redirect('company_dashboard')

    # Check if the company is approved
    if not company.approved:
        messages.error(request, "Your company must be approved by an admin to post internships.")
        return redirect('company_dashboard')

    if request.method == 'POST':
        form = InternshipPostingForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.company = company
            internship.save()
            messages.success(request, "Internship posted successfully.")
            return redirect('company_dashboard')
    else:
        form = InternshipPostingForm()

    return render(request, 'company_pages/post_internship.html', {
        'form': form,
        'current_page': 'post_internship'
    })


@login_required
def view_applicants(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id, company=request.user.company)
    applications = Application.objects.filter(internship=internship)
    return render(request, 'company_pages/view_applicants.html', {'applications': applications, 'internship': internship})


@login_required
def update_application_status(request, application_id, status):
    application = get_object_or_404(Application, id=application_id, internship__company=request.user.company)

    # Update the status if it's valid
    if status in ['Accepted', 'Rejected']:
        application.status = status
        application.save()
        messages.success(request, f'Application status updated to {status}.')
    else:
        messages.error(request, 'Invalid status update.')

    return redirect('view_applicants', internship_id=application.internship.id)


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
    if request.user.is_superuser == False:
        return redirect('home')
    elif request.user.is_superuser or request.user.user_type == 'Admin':
        return render(request, 'admin_pages/admin_dashboard.html', {'current_page': 'admin_dashboard'})