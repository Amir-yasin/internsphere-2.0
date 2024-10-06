from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type' ]

# Unregister the default User admin and register the custom one
admin.site.register(User, CustomUserAdmin)
admin.site.register(student_Profile)
admin.site.register(Company)
admin.site.register(CustomUser)


# from .models import *
# from .models import *
# from .models import *
# from .models import *
# from .models import *
# from .models import *
# from .models import *
# from .models import *
# from .models import *
# from .models import *