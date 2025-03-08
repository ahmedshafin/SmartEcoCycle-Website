# signup/serializers.py
from rest_framework import serializers
from .models import UserSignup,contactUsModel,PickupRequest, Recycler
from django.contrib.auth.models import User

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSignup
        fields = ['full_name', 'email', 'password', 'role', 'center_name', 'location', 'contact']


class contactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contactUsModel
        fields = ['contactFullName', 'contactEmail', 'contactPhoneNumber', 'contactSubject', 'contactMessage']




class PickupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupRequest
        fields = ['id', 'address', 'quantity', 'contact', 'latitude', 'longitude', 'status', 'created_at']





class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = contactUsModel
        fields = '__all__'


class RecyclerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recycler
        fields = '__all__'  # Includes all model fields
  