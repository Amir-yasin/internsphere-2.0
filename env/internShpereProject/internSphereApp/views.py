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
from datetime import date, timedelta
from django.db import transaction
from django.db.models import Subquery, OuterRef, Value, IntegerField



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
            elif user.user_type == 'Supervisor':
                return redirect('supervisor_dashboard')
            elif user.user_type == 'Department':
                return redirect('department_dashboard')
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
def Internships(request):
    return render(request, 'student_pages/Internships.html', {'current_page': 'Internships'})

@login_required
def student_profile(request):
    
    if not hasattr(request.user, 'stud_profile'):
        return redirect('error_page')  

    student = request.user.stud_profile

    if request.method == 'POST':
        student.email = request.POST.get('email', student.email)
        student.phone_number = request.POST.get('phone_number', student.phone_number)
        student.gender = request.POST.get('gender', student.gender)
        student.year_of_study = request.POST.get('year_of_study', student.year_of_study)
        student.skills = request.POST.get('skills', student.skills)
        student.resume = request.FILES.get('resume', student.resume)
        student.linkedin_profile = request.POST.get('linkedin_profile', student.linkedin_profile)
        student.department = request.POST.get('department', student.department)
        student.profile_completed = True  
        student.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('student_dashboard')

    return render(request, 'student_pages/student_profile.html', {
        'student': student,
        'department_choices': stud_profile.DEPARTMENT_CHOICES,
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
            return redirect('select_active_company')  

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

def view_biweekly_report(request, report_id):
    # Retrieve the report for viewing
    report = get_object_or_404(BiWeeklyReport, id=report_id)
    return render(request, 'company_pages/view_biweekly_report.html', {'report': report})


@login_required
def review_biweekly_reports(request):
    user = request.user

    # Initialize variables
    biweekly_reports = None
    final_reports = None
    evaluations = None

    # Filter reports and evaluations based on user type
    if user.user_type == "Company":
        biweekly_reports = BiWeeklyReport.objects.filter(company=user.company, company_approval_status="Pending")
        final_reports = FinalReport.objects.filter(company_approval_status="Pending")
        # evaluations = Evaluation.objects.filter(company=user.company)

    elif user.user_type == "InternshipCareerOffice":
        biweekly_reports = BiWeeklyReport.objects.filter(
            company_approval_status="Approved",
            internship_office_approval_status="Pending"
        )
        final_reports = FinalReport.objects.filter(company_approval_status="Approved",internship_office_approval_status="Pending")
        evaluations = Evaluation.objects.filter(internship_office_approval_status='Pending')

    elif user.user_type == "Department":
        biweekly_reports = BiWeeklyReport.objects.filter(
            internship_office_approval_status="Approved",
            department_approval_status="Pending",
            student__department=user.department_profile.department_name,
        )
        final_reports = FinalReport.objects.filter(
            internship_office_approval_status="Approved",
            department_approval_status="Pending"
        )
        evaluations = Evaluation.objects.filter(
            internship_office_approval_status='Approved',
            department_approval_status='Pending',
            student__department=user.department_profile.department_name
        )

    elif user.user_type == "Supervisor":
        biweekly_reports = BiWeeklyReport.objects.filter(
            department_approval_status="Approved",
            supervisor_approval_status="Pending",
            student__department=user.supervisor_profile.department.department_name,
        )
        final_reports = FinalReport.objects.filter(
            department_approval_status="Approved",
            supervisor_approval_status="Pending"
        )
        evaluations = Evaluation.objects.filter(
            department_approval_status='Approved',
            student__department=user.supervisor_profile.department.department_name
        )

    # Group reports and evaluations by student
    reports_by_student = {}
    if biweekly_reports:
        for report in biweekly_reports:
            student = report.student
            if student not in reports_by_student:
                reports_by_student[student] = {"biweekly": [], "final": [], "evaluations": []}
            reports_by_student[student]["biweekly"].append(report)

    if final_reports:
        for report in final_reports:
            student = report.student
            if student not in reports_by_student:
                reports_by_student[student] = {"biweekly": [], "final": [], "evaluations": []}
            reports_by_student[student]["final"].append(report)

    if evaluations:
        for evaluation in evaluations:
            student = evaluation.student
            if student not in reports_by_student:
                reports_by_student[student] = {"biweekly": [], "final": [], "evaluations": []}
            reports_by_student[student]["evaluations"].append(evaluation)

    # Render the template with the grouped data
    return render(request, "company_pages/review_biweekly_reports.html", {"reports_by_student": reports_by_student})


@login_required
def approve_biweekly_report(request, report_id, action):
    report = get_object_or_404(BiWeeklyReport, id=report_id)
    user = request.user

    if request.method == "POST":
        if action == "approve":
            if user.user_type == "Company":
                report.company_approval_status = "Approved"
                report.company_approval_date = now()
            elif user.user_type == "InternshipCareerOffice":
                report.internship_office_approval_status = "Approved"
                report.internship_office_approval_date = now()
            elif user.user_type == "Department":
                report.department_approval_status = "Approved"
                report.department_approval_date = now()
            elif user.user_type == "Supervisor":
                report.supervisor_approval_status = "Approved"
                report.supervisor_approval_date = now()
        elif action == "reject":
            if user.user_type == "Company":
                report.company_approval_status = "Rejected"
                report.company_approval_date = now()
            elif user.user_type == "InternshipCareerOffice":
                report.internship_office_approval_status = "Rejected"
                report.internship_office_approval_date = now()
            elif user.user_type == "Department":
                report.department_approval_status = "Rejected"
                report.department_approval_date = now()
            elif user.user_type == "Supervisor":
                report.supervisor_approval_status = "Rejected"
                report.supervisor_approval_date = now()

        report.save()
        return redirect("review_biweekly_reports")

    return render(request, "company_pages/approve_biweekly_report.html", {"report": report})

@login_required
def final_report(request):
    # Ensure only students can submit reports
    if request.user.user_type != 'Student':
        messages.error(request, "You do not have permission to submit a report.")
        return redirect('home')  # Replace 'home' with the appropriate URL
    try:
        # Ensure student profile exists and is completed
        student_profile = request.user.stud_profile
        if not student_profile.profile_completed:
            messages.error(request, 'Your profile is not completed yet!')
            return redirect('student_dashboard')

        # Check for the active company
        active_application = Application.objects.filter(student=student_profile, is_active=True).first()
        # print(active_application)
        if not active_application:
            messages.error(request, 'You have not selected a company to work with. Please select one.')
            return redirect('select_active_company')  

    except AttributeError:
        messages.error(request, 'Student profile is missing.')
        return redirect('student_profile')

    try:
        # Access the student's profile (assuming stud_profile is related to User)
        stud_profile_instance = request.user.stud_profile  # Access the related stud_profile instance

        # Check if the student has already submitted a report
        report_instance = FinalReport.objects.get(student=stud_profile_instance)
        form = FinalReportForm(request.POST or None, request.FILES or None, instance=report_instance)
    except FinalReport.DoesNotExist:
        form = FinalReportForm(request.POST or None, request.FILES or None)
    except stud_profile.DoesNotExist:
        # Handle the case where stud_profile doesn't exist for the user
        messages.error(request, "No profile found for the current user.")
        return redirect('home')

    if request.method == 'POST':
        if form.is_valid():
            final_report = form.save(commit=False)
            final_report.student = stud_profile_instance  # Set the related stud_profile instance
            final_report.save()
            messages.success(request, "Your final report has been submitted successfully!")
            return redirect('student_dashboard')  # Replace with the URL name for viewing the report
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'student_pages/final_report.html', {'form': form})



@login_required
def approve_final_report(request, report_id, action):
    final_report = get_object_or_404(FinalReport, id=report_id)
    user = request.user

    if request.method == "POST":
        if action == "approve":
            if user.user_type == "Company":
                final_report.company_approval_status = "Approved"
                final_report.company_approval_date = now()
            elif user.user_type == "InternshipCareerOffice":
                final_report.internship_office_approval_status = "Approved"
                final_report.internship_office_approval_date = now()
            elif user.user_type == "Department":
                final_report.department_approval_status = "Approved"
                final_report.department_approval_date = now()
            elif user.user_type == "Supervisor":
                final_report.supervisor_approval_status = "Approved"
                final_report.supervisor_approval_date = now()
        elif action == "reject":
            if user.user_type == "Company":
                final_report.company_approval_status = "Rejected"
                final_report.company_approval_date = now()
            elif user.user_type == "InternshipCareerOffice":
                final_report.internship_office_approval_status = "Rejected"
                final_report.internship_office_approval_date = now()
            elif user.user_type == "Department":
                final_report.department_approval_status = "Rejected"
                final_report.department_approval_date = now()
            elif user.user_type == "Supervisor":
                final_report.supervisor_approval_status = "Rejected"
                final_report.supervisor_approval_date = now()

        final_report.save()
        messages.success(request, f"Final report has been {action}d successfully!")
        return redirect("review_biweekly_reports")

    return render(request, "approve_final_report.html", {"final_report": final_report})

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
    return redirect('student_dashboard')

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
        try:
            student_profile = stud_profile.objects.get(user=request.user)
        except stud_profile.DoesNotExist:
            messages.error(request, "Student profile does not exist.")
            student_profile = None        
            return redirect('student_profile')
        internships = Internship.objects.filter(sector=student_profile.department, status='Open')
        company = Internship.objects.select_related('Company').all()
        context = {
            'company' : company,
            'internships': internships,
            'current_page': 'intern_opportunities'
        }
        return render(request, 'student_pages/intern_opportunities.html', context)
    except stud_profile.DoesNotExist:
        return redirect('student_profile')




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
            # Include error messages in the context if the form is invalid
            return render(request, 'company_pages/company_register.html', {
                'form': form,
                'current_page': 'company_register',
                'errors': form.errors
            })
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
    # Ensure the user is a company
    if not hasattr(request.user, 'company'):
        return render(request, 'home')
    company = request.user.company  # Assuming the user is linked to a company model
    interns = Internship.objects.filter(company=company)
    internships = company.internships.all()
    internship_list = [{'id': internship.id, 'title': internship.title} for internship in internships]
    active_applications = Application.objects.filter(company=company, is_active=True)
    students = stud_profile.objects.filter(applications__in=active_applications).distinct()

    students_with_internships = [
        {
            'student': application.student,  # Student linked to the application
            'internship': application.internship,  # Internship for the application
        }
        for application in active_applications
    ]

    context = {
        'internship_list': internship_list,  # List of internships for the company
        'students': students,  # Distinct list of students for evaluation
        'students_with_internships': students_with_internships,  # Students with their internships
        'interns': interns,
    }

    return render(request, 'company_pages/company_dashboard.html', context)


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
    # applicants = internship.applications.all()  # Fetch all applications for this internship
    applications = internship.applications.select_related('student__user')  # Optimized query

    # Filter pending applicants
    pending_applicants = applications.filter(status="Pending")
    
    return render(request, 'company_pages/view_applicants.html', {
        'internship': internship,
        # 'applicants': applicants,
        'applications': applications,
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

def attendance(request, student_id):
    student = get_object_or_404(stud_profile, id=student_id)
    today = date.today()
    start_date = today - timedelta(days=today.weekday())  # Start of the current week (Monday)
    dates = [(start_date - timedelta(weeks=w)) for w in range(8)]  # Generate start dates of past 8 weeks
    weeks = {w + 1: [(start_date - timedelta(weeks=w) + timedelta(d), None) for d in range(5)] for w in range(8)}

    # Populate attendance data
    for week, days in weeks.items():
        for i, (day, _) in enumerate(days):
            try:
                attendance = Attendance.objects.get(student=student, date=day)
                weeks[week][i] = (day, attendance.present)
            except Attendance.DoesNotExist:
                weeks[week][i] = (day, False)

    if request.method == 'POST':
        for week, days in weeks.items():
            for day, _ in days:
                date_str = day.strftime('%Y-%m-%d')
                present = request.POST.get(date_str) == 'on'  # Checked means 'on'
                attendance, created = Attendance.objects.get_or_create(student=student, date=day, defaults={'present': present})
                if not created:
                    attendance.present = present
                    attendance.save()
        messages.success(request, "Attendance marked successfully!")
        return redirect('attendance', student_id=student.id)

    context = {
        'student': student,
        'weeks': weeks,
    }
    return render(request, 'company_pages/attendance.html', context)


def attendance_list(request):
    company = request.user.company  # Ensure logged-in user is a company
    internships = Internship.objects.all
    active_applications = Application.objects.filter(company=company, is_active=True)
    students = [app.student for app in active_applications]
    return render(request, "company_pages/attendance_list.html", {"students": students , "internships": internships})


@login_required
def accepted_interns(request):
    return render(request, 'company_pages/accepted_interns.html', {'current_page': 'accepted_interns'})

@login_required
def submit_evaluation(request, student_id, internship_id):
    student = get_object_or_404(stud_profile, id=student_id)
    internship = get_object_or_404(Internship, id=internship_id)
    company = request.user.company  # Assuming logged-in user is a company

    # Check if an evaluation already exists
    if Evaluation.objects.filter(student=student, company=company, internship=internship).exists():
        messages.error(request, "You have already submitted an evaluation for this student.")
        return redirect('evaluation_list')

    if request.method == "POST":
        form = EvaluationForm(request.POST)
        if form.is_valid():
            total_raw_score = 0
            answered_questions = 0  # Track only answered questions (1-5)

            with transaction.atomic():  # Ensure atomic save
                evaluation = Evaluation.objects.create(
                    student=student,
                    internship=internship,
                    company=company,
                    total_score=0  # Temporary value, will update after calculation
                )

                for question in EvaluationQuestion.objects.all():
                    field_name = f'question_{question.id}'
                    answer_value = form.cleaned_data.get(field_name)

                    if answer_value != 'N/A':  # Exclude N/A responses
                        answered_questions += 1
                        total_raw_score += int(answer_value)

                        # Save individual answers
                        EvaluationAnswer.objects.create(
                            evaluation=evaluation,
                            question=question,
                            answer=int(answer_value)
                        )

                # Adjust calculation based on answered questions
                if answered_questions > 0:
                    evaluation.total_score = round((total_raw_score / answered_questions) * 10, 2)
                else:
                    evaluation.total_score = 0  # No valid answers, total score remains 0

                evaluation.save()

            messages.success(request, "Evaluation submitted successfully.")
            return redirect('evaluation_list')  # Redirect after submission

    else:
        form = EvaluationForm()

    return render(request, 'company_pages/submit_evaluation.html', {
        'form': form,
        'student': student,
        'internship': internship,
    })




@login_required
def evaluation_list(request):
    user = request.user

    if hasattr(user, 'company'):
        evaluations = Evaluation.objects.filter(company=user.company)
    elif user.user_type == 'InternshipCareerOffice':
        evaluations = Evaluation.objects.filter(internship_office_approval_status='Pending')
    elif user.user_type == 'Department':
        evaluations = Evaluation.objects.filter(internship_office_approval_status='Approved', department_approval_status='Pending')
    elif user.user_type == 'Supervisor':
        evaluations = Evaluation.objects.filter(department_approval_status='Approved')
    else:
        evaluations = None

    return render(request, 'company_pages/evaluation_list.html', {'evaluations': evaluations})


@login_required
def view_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    answers = EvaluationAnswer.objects.filter(evaluation=evaluation)

    return render(request, 'company_pages/view_evaluation.html', {
        'evaluation': evaluation,
        'answers': answers,
    })



def approve_evaluation(request, evaluation_id, action):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    user = request.user

    if request.method == 'POST':
        if action not in ('approve', 'reject'):
            messages.error(request, "Invalid action.")
            return redirect('evaluation_list')

        if user.user_type == 'InternshipCareerOffice':
            if action == 'approve':
                evaluation.internship_office_approval_status = 'Approved'
                evaluation.internship_office_approval_date = now()
            else:
                evaluation.internship_office_approval_status = 'Rejected'
                evaluation.internship_office_approval_date = now()
        elif user.user_type == 'Department':
            if action == 'approve':
                evaluation.department_approval_status = 'Approved'
                evaluation.department_approval_date = now()
            else:
                evaluation.department_approval_status = 'Rejected'
                evaluation.department_approval_date = now()

        # Save the evaluation status and redirect
        evaluation.save()
        messages.success(request, f"Evaluation has been {action}d.")
        return redirect('evaluation_list')

    return render(request, 'company_pages/approve_evaluation.html', {'evaluation': evaluation})


@login_required
def bulk_approve_evaluations(request):
    if request.user.user_type != 'InternshipCareerOffice':
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('dashboard')

    if request.method == 'POST':
        evaluation_ids = request.POST.getlist('evaluation_ids')  # IDs of evaluations to approve
        evaluations = Evaluation.objects.filter(id__in=evaluation_ids, internship_office_approval_status='Pending')
        evaluations.update(
            internship_office_approval_status='Approved',
            internship_office_approval_date=now()
        )
        messages.success(request, f"{evaluations.count()} evaluations approved successfully.")
        return redirect('evaluation_list')

    evaluations = Evaluation.objects.filter(internship_office_approval_status='Pending')
    return render(request, 'evaluations/bulk_approve.html', {'evaluations': evaluations})

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
    if request.user.user_type != 'InternshipCareerOffice':
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
def dis_approve_company(request, company_id):
    # company = get_object_or_404(company, id=company_id)
    # company.user.delete()  
    if request.user.is_superuser: 
        company = get_object_or_404(Company, id=company_id)
        company.approved = False
        company.save()
        messages.success(request, f"{company.company_name} has been dis-approved.")
    return redirect('approve_companies')

@login_required
def delete_company(request, company_id):
    company = get_object_or_404(company, id=company_id)
    company.user.delete()  

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def register_internship_career_office(request):
    if request.method == 'POST':
        form = InternshipCareerOfficeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('icu_list')  # Redirect to a page listing all career offices or a success page
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


# Dashboard view for Internship Career Office
@login_required
def department_dashboard(request):
    if request.user.user_type != 'Department':
        messages.error(request, "You do not have access to this page.")
        return redirect('home')

    students = stud_profile.objects.all()
    reports = BiWeeklyReport.objects.all()
    final_reports = FinalReport.objects.all()
    evaluations = Evaluation.objects.all()
    attendance_records = Attendance.objects.all()

    return render(request, 'department_pages/department_dashboard.html', {
        'students': students,
        'reports': reports,
        'final_reports': final_reports,
        'evaluations': evaluations,
        'attendance_records': attendance_records,
    })
    
    
@login_required
def supervisor_dashboard(request):
    if request.user.user_type != 'Supervisor':
        messages.error(request, "You do not have access to this page.")
        return redirect('home')

    students = stud_profile.objects.all()
    reports = BiWeeklyReport.objects.all()
    final_reports = FinalReport.objects.all()
    evaluations = Evaluation.objects.all()
    attendance_records = Attendance.objects.all()

    return render(request, 'supervisor_pages/supervisor_dashboard.html', {
        'students': students,
        'reports': reports,
        'final_reports': final_reports,
        'evaluations': evaluations,
        'attendance_records': attendance_records,
    })
    
  
    
@login_required
def view_applicants_list(request):
    user = request.user

    # Get all internships for the company
    internships = Internship.objects.filter(company=user.company)

    # Create a dictionary where each internship is mapped to its applications
    internship_applications = {
        internship: Application.objects.filter(internship=internship)
        for internship in internships
    }

    context = {
        'internship_applications': internship_applications,
    }
    return render(request, 'company_pages/view_applicants_list.html', context)


@login_required
def submit_evaluation_list(request):
    user = request.user
    students_with_internships = Application.objects.filter(company=user.company, is_active=True).select_related('student', 'internship')

    context = {
        'students_with_internships': students_with_internships, 
    }
    return render(request, 'company_pages/submit_evaluation_list.html', context)







@login_required
def assign_supervisor_view(request):
    if request.method == "POST":
        section_batch = request.POST.get("section_batch")
        supervisor_id = request.POST.get("supervisor_id")

        if not section_batch or not supervisor_id:
            messages.error(request, "Please select a valid section and supervisor.")
            return redirect("assign_supervisor")

        section, batch = section_batch.split("|")  # Extract section and batch from combined value

        students = stud_profile.objects.filter(section=section, batch=batch)
        supervisor = get_object_or_404(Supervisor, id=supervisor_id)

        if not students.exists():
            messages.error(request, "No students found in the selected section and batch.")
            return redirect("assign_supervisor")

        # Check if the section and batch already have an assigned supervisor
        existing_assignment = SupervisorAssignment.objects.filter(student__section=section, student__batch=batch).first()

        if existing_assignment:
            # Update the supervisor for all students in the section and batch
            SupervisorAssignment.objects.filter(student__section=section, student__batch=batch).update(supervisor=supervisor)
            messages.success(request, f"Supervisor updated for section {section}, batch {batch}.")
        else:
            # Assign the supervisor if not already assigned
            for student in students:
                SupervisorAssignment.objects.create(student=student, supervisor=supervisor)
            messages.success(request, f"Supervisor assigned successfully for section {section}, batch {batch}.")

        return redirect("assign_supervisor")

    # Get supervisors based on department
    department_name = request.user.department_profile.department_name
    supervisors = Supervisor.objects.filter(department__department_name=department_name)

    # Fetch unique section-batch combinations that have registered students
    section_batches = (
        stud_profile.objects.values_list('section', 'batch')
        .distinct()
        .order_by('section', 'batch')
    )

    return render(request, 'department_pages/assign_supervisor.html', {
        'supervisors': supervisors,
        'section_batches': section_batches,
    })






@login_required
def evaluation_view(request):
    supervisor = get_object_or_404(Supervisor, user=request.user)

    # Get all students assigned to this supervisor
    assigned_students = stud_profile.objects.filter(
        supervisor_assignment__supervisor=supervisor
    )

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        student = get_object_or_404(stud_profile, id=student_id)

        bi_weekly_score = request.POST.get(f"bi_weekly_report_score_{student.id}")
        final_report_score = request.POST.get(f"final_report_score_{student.id}")
        presentation_score = request.POST.get(f"presentation_score_{student.id}")

        if bi_weekly_score and final_report_score and presentation_score:
            try:
                bi_weekly_score = int(bi_weekly_score)
                final_report_score = int(final_report_score)
                presentation_score = int(presentation_score)

                if 0 <= bi_weekly_score <= 100 and 0 <= final_report_score <= 100 and 0 <= presentation_score <= 100:
                    evaluation, created = SupervisorEvaluation.objects.get_or_create(
                        student=student,
                        supervisor=supervisor
                    )

                    # Fetch the latest company evaluation manually
                    latest_company_evaluation = (
                        Evaluation.objects.filter(student=student)
                        .order_by('-submitted_at')
                        .first()
                    )

                    company_score = latest_company_evaluation.total_score if latest_company_evaluation else 0

                    evaluation.bi_weekly_report_score = bi_weekly_score
                    evaluation.final_report_score = final_report_score
                    evaluation.presentation_score = presentation_score

                    evaluation.total_score = (
                        bi_weekly_score + final_report_score + presentation_score + company_score
                    )

                    evaluation.save()

            except ValueError:
                print(f"Invalid score values for student {student.id}")

        return redirect('evaluation_view')

    # Fetch company evaluation scores manually for template rendering
    student_evaluations = {
        student.id: (
            Evaluation.objects.filter(student=student)
            .order_by('-submitted_at')
            .values('total_score')
            .first() or {'total_score': 0}
        )['total_score']
        for student in assigned_students
    }

    return render(request, "supervisor_pages/evaluation_page.html", {
        "students": assigned_students,
        "student_evaluations": student_evaluations,  # Pass evaluations to the template
    })
