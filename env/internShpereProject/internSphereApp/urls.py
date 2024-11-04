from django.urls import path
from . import views

urlpatterns = [  
# main pages url
path('', views.home , name = 'home'),
path('about', views.about , name = 'about'),
path('contact', views.contact , name = 'contact'),
path('login', views.login_user , name = 'login'),
path('accounts/login/', views.login_user , name = 'login'),
path('register', views.register_user , name = 'register'),
path('logout', views.logout, name='logout'),

# path('services', views.services , name = 'services'),


# student pages url
path('Graduate_students', views.Graduate_students , name = 'Graduate_students'),
path('intern_opportunities', views.intern_opportunities , name = 'intern_opportunities'),
path('Internships', views.Internships , name = 'Internships'),
path('student_profile', views.student_profile , name = 'student_profile'),
path('view_profile/<int:user_id>/', views.view_profile, name='view_profile'),
path('bi_weekly_report', views.bi_weekly_report , name = 'bi_weekly_report'),
path('student_dashboard', views.student_dashboard , name = 'student_dashboard'),
path('applications', views.applications , name = 'applications'),
path('stud_notification', views.stud_notification , name = 'stud_notification'),


# company pages url
path('post_internship', views.post_internship , name = 'post_internship'),
path('company_dashboard', views.company_dashboard , name = 'company_dashboard'),
path('company_profile', views.Company , name = 'Company'),
path('view_applicants', views.view_applicants , name = 'view_applicants'),
path('attendance', views.attendance , name = 'attendance'),
path('accepted_interns', views.accepted_interns , name = 'accepted_interns'),
path('evaluate_intern', views.evaluate_intern , name = 'evaluate_intern'),



path('register_students', views.register_students , name = 'register_students'),
path('admin_dashboard', views.admin_dashboard , name = 'admin_dashboard'),
path('student_list', views.student_list , name = 'student_list'),
path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),
# path('attendance', views.attendance , name = 'attendance'),





]