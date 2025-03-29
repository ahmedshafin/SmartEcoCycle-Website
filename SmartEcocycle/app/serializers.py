# signup/serializers.py
from rest_framework import serializers
from .models import UserSignup,contactUsModel,PickupRequest, RecyclerCreate
from django.contrib.auth.models import User
from rest_framework.serializers import Serializer, CharField, EmailField, FloatField, IntegerField
#Grok
class UserSignupSerializer(Serializer):
    email = EmailField(required=True)
    full_name = CharField(max_length=255, required=True)
    role = CharField(max_length=50, required=True)
    password = CharField(max_length=128, write_only=True, required=True)
    rating = FloatField(default=5.0, required=False)
    total_pickup = IntegerField(default=0, required=False)
    total_recycled = FloatField(default=0.0, required=False)

    def create(self, validated_data):
        # Extract password and hash it using the model's manager
        password = validated_data.pop('password')
        user = UserSignup.objects.create_user(
            email=validated_data['email'],
            password=password,
            full_name=validated_data['full_name'],
            role=validated_data['role'],
            rating=validated_data.get('rating', 0.0),
            total_pickup=validated_data.get('total_pickup', 0),
            total_recycled=validated_data.get('total_recycled', 0.0)
        )
        return user

    def validate_email(self, value):
        # Ensure email is unique
        if UserSignup.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class contactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contactUsModel
        fields = ['contactFullName', 'contactEmail', 'contactPhoneNumber', 'contactSubject', 'contactMessage']




class PickupRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(  # Change from PrimaryKeyRelatedField to HiddenField
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = PickupRequest
        fields = [
            'id', 'user', 'address', 'quantity', 'contact',
            'latitude', 'longitude', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'status']

    
    def create(self, validated_data):
        print(f"Creating PickupRequest with validated data: {validated_data}")
        return PickupRequest.objects.create(**validated_data)

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = contactUsModel
        fields = '__all__'


  
class RecyclerLoginSerializer(serializers.Serializer):
    contact_number = serializers.CharField()
    password = serializers.CharField(write_only=True)



class RecyclerSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = RecyclerCreate
        fields = ['id', 'name', 'contact_number', 'assigned_area', 'status', 'password']


#Recycler Login
class RecyclerLoginSerializer(serializers.Serializer):
    contact_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)