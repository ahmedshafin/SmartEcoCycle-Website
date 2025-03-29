from django.contrib import admin
from .models import *


class UserSignupAdmin(admin.ModelAdmin):
    list_display = ('id','full_name', 'email', 'role','total_pickup', 'total_recycled', 'rating')

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



@admin.register(assigned_recycler)
class AssignedRecyclerAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'address', 'quantity', 'latitude', 'longitude')
    list_filter = ('status',)
    search_fields = ('name', 'address')
    ordering = ('name',)





class RecyclerCreateAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('name', 'contact_number', 'assigned_area', 'status', 'password')
    # Filter by 'status' in the admin interface
    list_filter = ('status',)
    # Add search functionality for 'name' and 'contact_number'
    search_fields = ('name', 'contact_number')
    # Allow ordering by 'name' in ascending order
    ordering = ('name',)
    # Add form fieldsets if you need to structure the form better
    fieldsets = (
        (None, {
            'fields': ('name', 'contact_number', 'assigned_area', 'status', 'password')
        }),
    )

    # Optionally, to make password field read-only in admin, use below:
    def save_model(self, request, obj, form, change):
        # Ensure password is always saved as a hashed value
        if not obj.password.startswith('pbkdf2_sha256$'):
            # For example, using Django's make_password method to hash the password before saving
            from django.contrib.auth.hashers import make_password
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

# Register the RecyclerCreate model with the custom admin configuration
admin.site.register(RecyclerCreate, RecyclerCreateAdmin)




