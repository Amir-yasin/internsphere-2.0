from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', ]

# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Company)


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