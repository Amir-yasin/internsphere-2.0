from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type' ]
    search_fields = ['username','email', 'phone_number','section','batch','department','user_type']

# Unregister the default User admin and register the custom one
admin.site.register(User, CustomUserAdmin)
admin.site.register(stud_profile)
admin.site.register(Company)
admin.site.register(CustomUser)
admin.site.register(Internship)
admin.site.register(BiWeeklyReport)
admin.site.register(FinalReport)
admin.site.register(Application)
admin.site.register(Evaluation)
admin.site.register(EvaluationQuestion)
admin.site.register(EvaluationAnswer)


@admin.register(InternshipCareerOffice)
class InternshipCareerOfficeAdmin(admin.ModelAdmin):
    list_display = ['user', 'ICU_director']
    search_fields = ['user__username', 'ICU_director']
# admin.site.register(Company)
# admin.site.register(Company)
# admin.site.register(Company)




import pandas as pd
from django.core.exceptions import ValidationError

# Function to handle bulk student upload
def upload_students_from_excel(file):
    df = pd.read_excel(file)
    for _, row in df.iterrows():
        user = CustomUser.objects.create_user(
            username=row['email'],
            email=row['email'],
            user_type='Student',
            password='temporary_password'  # Set default password
        )
        StudentProfile.objects.create(
            user=user,
            batch=row['batch'],
            section=row['section'],
            temporary_password='temporary_password'
        )
