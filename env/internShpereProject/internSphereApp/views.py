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
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.utils.timezone import now


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
            elif user.user_type == 'InternshipCareerOffice':
                return redirect('icu_dashboard')
            else:
                return redirect('homes')
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
    try:
        # Ensure student profile exists and is completed
        student_profile = request.user.stud_profile
        if not student_profile.profile_completed:
            messages.error(request, 'Your profile is not completed yet!')
            return redirect('student_dashboard')

        # Check for the active company
        active_application = Application.objects.filter(student=student_profile, is_active=True).first()

        if not active_application:
            messages.error(request, 'You have not selected a company to work with. Please select one.')
            return redirect('select_active_company')  # Redirect to company selection page

    except AttributeError:
        messages.error(request, 'Student profile is missing.')
        return redirect('student_profile')

    if request.method == 'POST':
        form = BiWeeklyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.student = student_profile  # Associate the student profile
            report.company = active_application.company  # Use the active company
            report.application_status = active_application  # Associate the application
            report.save()
            messages.success(request, 'Bi-weekly report submitted successfully!')
            return redirect('student_dashboard')
    else:
        form = BiWeeklyReportForm()

    context = {
        'form': form,
        'id_number': student_profile.id,
        'company': active_application.company.company_name if active_application else None,
        'section': student_profile.section,
        'current_page': 'bi_weekly_report',
    }
    return render(request, 'student_pages/bi_weekly_report.html', context)


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
def select_active_company(request):
    student_profile = request.user.stud_profile
    accepted_applications = Application.objects.filter(student=student_profile, status='Accepted')

    if request.method == 'POST':
        selected_application_id = request.POST.get('application_id')
        if selected_application_id:
            # Reset all other applications to inactive
            Application.objects.filter(student=student_profile).update(is_active=False)
            # Set the selected application as active
            selected_application = get_object_or_404(Application, id=selected_application_id)
            selected_application.is_active = True
            selected_application.save()
            messages.success(request, f"You've successfully selected {selected_application.company.company_name} as your active company.")
            return redirect('student_dashboard')

    context = {
        'accepted_applications': accepted_applications,
    }
    return render(request, 'student_pages/select_active_company.html', context)

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
    internships = Internship.objects.filter(company=request.user.company)
    internship_list = [{'id': internship.id, 'title': internship.title} for internship in internships]
    return render(request, 'company_pages/company_dashboard.html', {'internship_list': internship_list})


@login_required
def post_internship(request):
    try:
        company = request.user.company
    except Company.DoesNotExist:
        messages.error(request, "You need a company profile to post internships.")
        return redirect('company_dashboard')

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
    internship = get_object_or_404(Internship, id=internship_id)
    applicants = internship.applications.all()  # Fetch all applications for this internship
    
    # Filter pending applicants
    pending_applicants = applicants.filter(status="Pending")
    
    return render(request, 'company_pages/view_applicants.html', {
        'internship': internship,
        'applicants': applicants,
        'pending_applicants': pending_applicants,
    })
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
    



    # internship and carrer office views


# Dashboard view for Internship Career Office
@login_required
def icu_dashboard(request):
    if request.user.customuser.user_type != 'InternshipCareerOffice':
        messages.error(request, "You do not have access to this page.")
        return redirect('home')

    students = stud_profile.objects.all()
    reports = BiWeeklyReport.objects.all()
    evaluations = Evaluation.objects.all()
    attendance_records = Attendance.objects.all()

    return render(request, 'internship_office_pages/icu_dashboard.html', {
        'students': students,
        'reports': reports,
        'evaluations': evaluations,
        'attendance_records': attendance_records,
    })
    
# Department dashboard view
@login_required
def department_dashboard(request):
    if request.user.customuser.user_type != 'Department':
        messages.error(request, "You do not have access to this page.")
        return redirect('home')

    department = get_object_or_404(Department, user=request.user)
    students = stud_profile.objects.filter(department=department.department_name)

    return render(request, 'department_dashboard.html', {
        'department': department,
        'students': students,
    })


# Supervisor dashboard view
@login_required
def supervisor_dashboard(request):
    if request.user.customuser.user_type != 'Supervisor':
        messages.error(request, "You do not have access to this page.")
        return redirect('home')

    supervisor = get_object_or_404(Supervisor, user=request.user)
    supervised_students = stud_profile.objects.filter(department=supervisor.department)

    return render(request, 'supervisor_dashboard.html', {
        'supervisor': supervisor,
        'supervised_students': supervised_students,
    })


# Internship listing view
@login_required
def internship_list(request):
    internships = Internship.objects.filter(status='Open').order_by('-posted_on')

    return render(request, 'internship_list.html', {
        'internships': internships,
    })



# View for ICU to send reports to the department
@login_required
def send_reports_to_department(request):
    if request.user.customuser.user_type != 'InternshipCareerOffice':
        messages.error(request, "You do not have permission to send reports.")
        return redirect('home')

    reports = BiWeeklyReport.objects.all()
    # Additional logic to send reports can be added here, such as sending an email to department

    messages.success(request, "Reports sent to the department.")
    return redirect('icu_dashboard')


# Function to close internships if expired
def close_expired_internships():
    internships = Internship.objects.filter(status='Open')
    for internship in internships:
        if internship.is_expired():
            internship.close_if_expired()

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


def is_admin(user):
    return user.is_authenticated and user.user_type == 'Admin'

@user_passes_test(is_admin)
def register_internship_career_office(request):
    if request.method == 'POST':
        form = InternshipCareerOfficeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('career_office_list')  # Redirect to a page listing all career offices or a success page
    else:
        form = InternshipCareerOfficeForm()
    return render(request, 'admin_pages/register_internship_career_office.html', {'form': form})


@login_required
def icu_list(request):
    icu_list = InternshipCareerOffice.objects.all()
    return render(request, 'admin_pages/icu_list.html', {'icu_list': icu_list})

@login_required
def register_department(request):
    if not request.user.is_superuser:  # Only allow superusers to register departments
        messages.error(request, "You do not have permission to register a department.")
        return redirect('home')  # Replace 'home' with the appropriate URL name

    if request.method == "POST":
        form = DepartmentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Department registered successfully!")
                return redirect('department_list')  # Replace with the URL name for department list
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DepartmentRegistrationForm()

    return render(request, 'admin_pages/register_department.html', {'form': form})

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'admin_pages/department_list.html', {'departments': departments})


@login_required
def register_supervisor(request):
    if not request.user.is_superuser:  # Only allow superusers to register supervisors
        messages.error(request, "You do not have permission to register a supervisor.")
        return redirect('home')  # Replace 'home' with the appropriate URL name

    if request.method == "POST":
        form = SupervisorRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Supervisor registered successfully!")
                return redirect('supervisor_list')  # Replace with the URL name for supervisor list
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SupervisorRegistrationForm()

    return render(request, 'admin_pages/register_supervisor.html', {'form': form})

@login_required
def supervisor_list(request):
    supervisors = Supervisor.objects.all()
    return render(request, 'admin_pages/supervisor_list.html', {'supervisors': supervisors})