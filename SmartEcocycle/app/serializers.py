# signup/serializers.py
from rest_framework import serializers
from .models import UserSignup

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSignup
        fields = ['full_name', 'email', 'password', 'role', 'center_name', 'location', 'contact']

    