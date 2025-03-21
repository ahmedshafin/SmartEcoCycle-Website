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


@admin.register(Recycler)
class RecyclerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'assigned_area', 'status', 'created_at')
    list_filter = ('status', 'assigned_area')
    search_fields = ('name', 'contact_number', 'assigned_area')
    ordering = ('-created_at',)
    list_per_page = 20  # Pagination for better readability

@admin.register(assigned_recycler)
class AssignedRecyclerAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'address', 'quantity', 'latitude', 'longitude')
    list_filter = ('status',)
    search_fields = ('name', 'address')
    ordering = ('name',)




