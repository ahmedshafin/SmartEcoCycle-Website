# serializers.py
from rest_framework import serializers

class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    dob = serializers.DateField()
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    def validate(self, data):
        # Check if the passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
