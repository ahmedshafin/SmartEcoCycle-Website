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
