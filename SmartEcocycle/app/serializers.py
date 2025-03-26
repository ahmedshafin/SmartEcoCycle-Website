# signup/serializers.py
from rest_framework import serializers
from .models import UserSignup,contactUsModel,PickupRequest, RecyclerCreate
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


  
class RecyclerLoginSerializer(serializers.Serializer):
    contact_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


#New approach
class RecyclerSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = RecyclerCreate
        fields = ['id', 'name', 'contact_number', 'assigned_area', 'status', 'password']


#Recycler Login
class RecyclerLoginSerializer(serializers.Serializer):
    contact_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)