# signup/admin.py
from django.contrib import admin
from .models import *

class UserSignupAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'password', 'role')

admin.site.register(UserSignup, UserSignupAdmin)



class contactUsAdmin(admin.ModelAdmin):
    list_display = ('contactFullName', 'contactEmail', 'contactPhoneNumber', 'contactSubject', 'contactMessage')

admin.site.register(contactUsModel, contactUsAdmin)
