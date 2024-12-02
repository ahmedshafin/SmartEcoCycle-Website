# signup/admin.py
from django.contrib import admin
from .models import UserSignup

class UserSignupAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'password', 'role')

admin.site.register(UserSignup, UserSignupAdmin)
