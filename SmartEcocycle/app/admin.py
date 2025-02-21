# signup/admin.py
from django.contrib import admin
from .models import *

class UserSignupAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'password', 'role')

admin.site.register(UserSignup, UserSignupAdmin)



class contactUsAdmin(admin.ModelAdmin):
    list_display = ('contactFullName', 'contactEmail', 'contactPhoneNumber', 'contactSubject', 'contactMessage')

admin.site.register(contactUsModel, contactUsAdmin)



class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ('address', 'quantity', 'contact', 'latitude', 'longitude', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('address', 'quantity', 'contact')
    ordering = ('-created_at',)
    fields = ('address', 'quantity', 'contact', 'latitude', 'longitude', 'status', 'created_at')
    readonly_fields = ('created_at',)  # This ensures the created_at field is not editable

admin.site.register(PickupRequest, PickupRequestAdmin)



