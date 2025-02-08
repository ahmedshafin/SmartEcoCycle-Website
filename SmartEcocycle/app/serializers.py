# signup/serializers.py
from rest_framework import serializers
from .models import UserSignup,contactUsModel
from django.contrib.auth.models import User

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSignup
        fields = ['full_name', 'email', 'password', 'role', 'center_name', 'location', 'contact']


class contactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contactUsModel
        fields = ['contactFullName', 'contactEmail', 'contactPhoneNumber', 'contactSubject', 'contactMessage']








    