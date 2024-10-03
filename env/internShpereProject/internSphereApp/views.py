from django.shortcuts import render

# Create your views here.
# main pages views

def home(request):
    return render(request, 'main_pages/index.html', {'current_page': 'home'})
def about(request):
    return render(request, 'main_pages/About.html', {'current_page': 'about'})
def contact(request):
    return render(request, 'main_pages/contact.html', {'current_page': 'contact'})
def login(request):
    return render(request, 'main_pages/login.html', {'current_page': 'login'})
def register(request):
    return render(request, 'main_pages/register.html', {'current_page': 'register'})
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

