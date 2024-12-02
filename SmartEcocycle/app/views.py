# signup/views.py
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserSignup
from .serializers import UserSignupSerializer


#homepage
def viewHomepage(request):
    return render(request, 'index.html')


#success message
def success(request):
    return render(request, 'success.html')

def signup_form_page(request):
    return render(request, 'register.html')




# If you want to handle the API endpoint using DRF
class UserSignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
