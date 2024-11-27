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
path('student_profile', views.stud_profile , name = 'student_profile'),
path('view_profile/<int:user_id>/', views.view_profile, name='view_profile'),
path('bi_weekly_report', views.bi_weekly_report , name = 'bi_weekly_report'),
path('final_report', views.final_report, name='final_report'),
path('student_dashboard', views.student_dashboard , name = 'student_dashboard'),
path('apply_to_internship/<int:internship_id>/apply/', views.apply_to_internship, name='apply_to_internship'),
path('applications', views.applications, name='applications'),
path('stud_notification', views.stud_notification , name = 'stud_notification'),
path('select_active_company', views.select_active_company , name = 'select_active_company'),

# path('api/internships/', views.internships_by_department, name='internships_by_department'),

# company pages url
path('post_internship', views.post_internship , name = 'post_internship'),
path('company_dashboard', views.company_dashboard , name = 'company_dashboard'),
path('company_register', views.company_register , name = 'company_register'),
path('company/<int:user_id>/', views.view_company_profile, name='view_company_profile'),
# path('view_applicants/', views.view_applicants, name='view_applicants'), 
path('view_applicants/<int:internship_id>/', views.view_applicants, name='view_applicants'),
path('update_application_status/<int:application_id>/status/<str:status>/', views.update_application_status, name='update_application_status'),
path('attendance', views.attendance , name = 'attendance'),
path('accepted_interns', views.accepted_interns , name = 'accepted_interns'),
path('evaluate_intern', views.evaluate_intern , name = 'evaluate_intern'),
# path('reports/<str:approver_type>/<int:report_id>/approve/', views.approve_report, name='approve_report'),



#admin pages url(students)
path('admin_dashboard', views.admin_dashboard , name = 'admin_dashboard'),
path('register_students', views.register_students , name = 'register_students'),
path('student_list', views.student_list , name = 'student_list'),
path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),

#admin pages url(company)
path('approve_companies/', views.approve_companies, name='approve_companies'),
path('approve_company/<int:company_id>/', views.approve_company, name='approve_company'),
path('view_company_info/<int:company_id>/', views.view_company_info, name='view_company_info'),
path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),

# admin pages url(icu)
path('register-internship-career-office', views.register_internship_career_office, name='register_internship_career_office'),
path('icu_list', views.icu_list , name = 'icu_list'),

# admin pages url(department)
path('register/department', views.register_department, name='register_department'),
path('department_list', views.department_list , name = 'department_list'),

# admin pages url(supervisor)
path('register_supervisor', views.register_supervisor, name='register_supervisor'),
path('supervisor_list', views.supervisor_list , name = 'supervisor_list'),

#icu pages url
path('icu_dashboard', views.icu_dashboard , name = 'icu_dashboard'),

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