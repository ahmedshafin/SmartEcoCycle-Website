# signup/models.py
from django.db import models

class UserSignup(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    
    # Additional fields for Recycle Center
    center_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name
    

class contactUsModel(models.Model):
    contactFullName = models.CharField(max_length=50)
    contactEmail = models.CharField(max_length=50)
    contactPhoneNumber = models.CharField(max_length= 15)
    contactSubject = models.CharField(max_length=50)
    contactMessage = models.TextField()


class PickupRequest(models.Model):
    address = models.CharField(max_length=255, default="Unknown")
    quantity = models.CharField(max_length=50, default="Unknown")
    contact = models.CharField(max_length=15, default="Unknown")
    latitude = models.DecimalField(max_digits=9, decimal_places=7)
    longitude = models.DecimalField(max_digits=9, decimal_places=7)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pickup at {self.address} ({self.quantity})"
    

class assigned_recycler(models.Model):

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default='active')
    address = models.CharField(max_length=255, default="Unknown")
    quantity = models.CharField(max_length=50, default="Unknown")
    latitude = models.FloatField( null=True)
    longitude = models.FloatField( null=True)


# creating recyclers
class RecyclerCreate(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, unique=True)
    assigned_area = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    password = models.CharField(max_length=128)  # Store hashed passwords

    def __str__(self):
        return self.name

