# signup/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
#grok
#create superuser
class UserSignupManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes password
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        
        # Set default values for required fields if not provided
        if 'full_name' not in extra_fields:
            extra_fields['full_name'] = "Admin User"
        
        # Validate superuser flags
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class UserSignup(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, default='user')
    rating = models.FloatField(default=0.0)
    total_pickup = models.IntegerField(default=0)
    total_recycled = models.FloatField(default=0.0)
    
    # Add these fields for admin access
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UserSignupManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return self.is_superuser
    

class contactUsModel(models.Model):
    contactFullName = models.CharField(max_length=50)
    contactEmail = models.CharField(max_length=50)
    contactPhoneNumber = models.CharField(max_length= 15)
    contactSubject = models.CharField(max_length=50)
    contactMessage = models.TextField()

#Dynamic Update to user
class PickupRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Assigned', 'Assigned'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default="Unknown")
    quantity = models.CharField(max_length=50, default="Unknown")
    contact = models.CharField(max_length=15, default="Unknown")
    latitude = models.DecimalField(max_digits=9, decimal_places=7)
    longitude = models.DecimalField(max_digits=9, decimal_places=7)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

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
    name = models.CharField(max_length=100, unique=True)
    contact_number = models.CharField(max_length=15, unique=True)
    assigned_area = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    password = models.CharField(max_length=128)  # Store hashed passwords

    def __str__(self):
        return self.name

