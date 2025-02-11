from django.urls import path
from . import views

urlpatterns = [  
# main pages url
path('', views.home , name = 'home'),
path('about', views.about , name = 'about'),
path('contact', views.contact , name = 'contact'),
path('login', views.login_user , name = 'login'),
path('accounts/login/', views.login_user , name = 'login'),
path('logout', views.logout, name='logout'),


# student pages url
path('intern_opportunities', views.intern_opportunities , name = 'intern_opportunities'),
path('Internships', views.Internships , name = 'Internships'),
path('student_profile', views.student_profile, name='student_profile'),
path('view_profile/<int:user_id>/', views.view_profile, name='view_profile'),
path('bi_weekly_report', views.bi_weekly_report , name = 'bi_weekly_report'),
path('final_report', views.final_report, name='final_report'),
path('student_dashboard', views.student_dashboard , name = 'student_dashboard'),
path('apply_to_internship/<int:internship_id>/apply/', views.apply_to_internship, name='apply_to_internship'),
path('applications', views.applications, name='applications'),
path('Graduate_students', views.Graduate_students , name = 'Graduate_students'),
path('select_active_company', views.select_active_company , name = 'select_active_company'),


# company pages url
path('post_internship', views.post_internship , name = 'post_internship'),
path('company_dashboard', views.company_dashboard , name = 'company_dashboard'),
path('company_register', views.company_register , name = 'company_register'),
path('company/<int:user_id>/', views.view_company_profile, name='view_company_profile'),
path('view_applicants_list/', views.view_applicants_list, name='view_applicants_list'),
path('view_applicants/<int:internship_id>/', views.view_applicants, name='view_applicants'),
path('update_application_status/<int:application_id>/status/<str:status>/', views.update_application_status, name='update_application_status'),
path('attendance_list/', views.attendance_list, name='attendance_list'), 
path('accepted_interns', views.accepted_interns , name = 'accepted_interns'),
path('attendance/<int:student_id>/', views.attendance, name='attendance'),

path("approve_final_report/<int:report_id>/<str:action>/",views.approve_final_report,name="approve_final_report"),
path("review_biweekly_reports/", views.review_biweekly_reports, name="review_biweekly_reports"),
path('approve_biweekly_report/<int:report_id>/<str:action>/', views.approve_biweekly_report, name='approve_biweekly_report'),
path('biweekly-report/<int:report_id>/view/', views.view_biweekly_report, name='view_biweekly_report'),


#admin pages url(students)
path('admin_dashboard', views.admin_dashboard , name = 'admin_dashboard'),
path('register_students', views.register_students , name = 'register_students'),
path('student_list', views.student_list , name = 'student_list'),
path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
#admin pages url(company)
path('approve_companies/', views.approve_companies, name='approve_companies'),
path('approve_company/<int:company_id>/', views.approve_company, name='approve_company'),
path('view_company_info/<int:company_id>/', views.view_company_info, name='view_company_info'),
path('dis_approve_company/<int:company_id>/', views.dis_approve_company, name='dis_approve_company'),
path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),
# admin pages url(icu)
path('register-internship-career-office', views.register_internship_career_office, name='register_internship_career_office'),
path('icu_list', views.icu_list , name = 'icu_list'),
path('delete_icu/<int:InternshipCareerOffice_id>/', views.delete_icu, name='delete_icu'),

# admin pages url(department)
path('department', views.register_department, name='register_department'),
path('department_list', views.department_list , name = 'department_list'),
path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),

# admin pages url(supervisor)
path('register_supervisor', views.register_supervisor, name='register_supervisor'),
path('supervisor_list', views.supervisor_list , name = 'supervisor_list'),
path('delete_supervisor/<int:supervisor_id>/', views.delete_supervisor, name='delete_supervisor'),





#icu pages url
path('icu_dashboard', views.icu_dashboard , name = 'icu_dashboard'),
path("absent_students/", views.absent_students, name="absent_students"),




#department pages
path('department_dashboard', views.department_dashboard , name = 'department_dashboard'),
path("assign_supervisor", views.assign_supervisor_view, name="assign_supervisor"),




#supervisor pages
path('supervisor_dashboard', views.supervisor_dashboard , name = 'supervisor_dashboard'),
path("evaluation_view/", views.evaluation_view, name="evaluation_view"),
path('submit_evaluation_list/', views.submit_evaluation_list, name='submit_evaluation_list'),
path('submit_evaluation/<int:student_id>/<int:internship_id>/', views.submit_evaluation, name='submit_evaluation'),
path('approve_evaluation/<int:evaluation_id>/<str:action>/', views.approve_evaluation, name='approve_evaluation'),
path('evaluation/list/', views.evaluation_list, name='evaluation_list'),
path('view_evaluation/<int:evaluation_id>/', views.view_evaluation, name='view_evaluation'),


 
]


