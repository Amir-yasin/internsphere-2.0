from django.shortcuts import render

# Create your views here.
        # main pages
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
def services(request):
    return render(request, 'main_pages/services.html', {'current_page': 'services'})



# student pages


def Graduate_students(request):
    return render(request, 'student_pages/Graduate_students.html', {'current_page': 'Graduate_students'})
def intern_opportunities(request):
    return render(request, 'student_pages/intern_opportunities.html', {'current_page': 'intern_opportunities'})
def Internships(request):
    return render(request, 'student_pages/Internships.html', {'current_page': 'Internships'})

def student_profile(request):
    return render(request, 'student_pages/student_profile.html', {'current_page': 'student_profile'})
def company_dashboard(request):
    return render(request, 'company_pages/company_dashboard.html', {'current_page': 'company_dashboard'})
def bi_weekly_report(request):
    return render(request, 'student_pages/bi_weekly_report.html', {'current_page': 'bi_weekly_report'})
def company_profile(request):
    return render(request, 'company_pages/company_profile.html', {'current_page': 'company_profile'})
def student_dashboard(request):
    return render(request, 'student_pages/student_dashboard.html', {'current_page': 'student_dashboard'})
def applications(request):
    return render(request, 'student_pages/applications.html', {'current_page': 'applications'})
def stud_notification(request):
    return render(request, 'student_pages/stud_notification.html', {'current_page': 'stud_notification'})

# def stud_notification(request):
#     return render(request, 'stud_notification.html', {'current_page': 'stud_notification'})
# def stud_notification(request):
#     return render(request, 'stud_notification.html', {'current_page': 'stud_notification'})
# def stud_notification(request):
#     return render(request, 'stud_notification.html', {'current_page': 'stud_notification'})
# def stud_notification(request):
#     return render(request, 'stud_notification.html', {'current_page': 'stud_notification'