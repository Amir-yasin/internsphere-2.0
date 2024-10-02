from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html', {'current_page': 'home'})
def about(request):
    return render(request, 'About.html', {'current_page': 'about'})
def companies(request):
    return render(request, 'companies.html', {'current_page': 'companies'})
def contact(request):
    return render(request, 'contact.html', {'current_page': 'contact'})
def Graduate_students(request):
    return render(request, 'Graduate_students.html', {'current_page': 'Graduate_students'})
def intern_opportunities(request):
    return render(request, 'intern_opportunities.html', {'current_page': 'intern_opportunities'})
def Internships(request):
    return render(request, 'Internships.html', {'current_page': 'Internships'})
def login(request):
    return render(request, 'login.html', {'current_page': 'login'})
def register(request):
    return render(request, 'register.html', {'current_page': 'register'})
def services(request):
    return render(request, 'services.html', {'current_page': 'services'})
def student_profile(request):
    return render(request, 'student_profile.html', {'current_page': 'student_profile'})
def universities(request):
    return render(request, 'universities.html', {'current_page': 'universities'})
def bi_weekly_report(request):
    return render(request, 'bi_weekly_report.html', {'current_page': 'bi_weekly_report'})
def company_profile(request):
    return render(request, 'company_profile.html', {'current_page': 'company_profile'})
def student_dashboard(request):
    return render(request, 'student_dashboard.html', {'current_page': 'student_dashboard'})
def applications(request):
    return render(request, 'applications.html', {'current_page': 'applications'})
def stud_notification(request):
    return render(request, 'stud_notification.html', {'current_page': 'stud_notification'})
# def stud_notification(request):
#     return render(request, 'stud_notification.html', {'current_page': 'stud_notification'})
# def stud_notification(request):
#     return render(request, 'stud_notification.html', {'current_page': 'stud_notification'})
# def stud_notification(request):
#     return render(request, 'stud_notification.html', {'current_page': 'stud_notification'})
# def stud_notification(request):
#     return render(request, 'stud_notification.html', {'current_page': 'stud_notification'})