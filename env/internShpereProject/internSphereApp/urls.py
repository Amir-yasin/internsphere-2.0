from django.urls import path
from . import views

urlpatterns = [
path('', views.home , name = 'home'),
path('about', views.about , name = 'about'),
path('companies', views.companies , name = 'companies'),
path('contact', views.contact , name = 'contact'),
path('Graduate_students', views.Graduate_students , name = 'Graduate_students'),
path('intern_opportunities', views.intern_opportunities , name = 'intern_opportunities'),
path('Internships', views.Internships , name = 'Internships'),
path('login', views.login , name = 'login'),
path('register', views.register , name = 'register'),
path('services', views.services , name = 'services'),
path('student_profile', views.student_profile , name = 'student_profile'),
path('universities', views.universities , name = 'universities'),
path('bi_weekly_report', views.bi_weekly_report , name = 'bi_weekly_report'),
path('company_profile', views.company_profile , name = 'company_profile'),
path('student_dashboard', views.student_dashboard , name = 'student_dashboard'),
path('applications', views.applications , name = 'applications'),
path('stud_notification', views.stud_notification , name = 'stud_notification'),
# path('student_profile', views.student_profile , name = 'student_profile'),



]