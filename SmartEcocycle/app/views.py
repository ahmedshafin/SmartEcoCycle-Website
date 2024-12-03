# signup/views.py
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserSignup
from .serializers import UserSignupSerializer
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password

#homepage
def viewHomepage(request):
    return render(request, 'index.html')


#fail message
def fail(request):
    return render(request, 'fail.html')

def signup_form_page(request):
    return render(request, 'register.html')


# If you want to handle the API endpoint using DRF
class UserSignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Redirect to the homepage on success
            return HttpResponseRedirect(redirect_to='/')
        # Redirect to the unsuccessful page on failure
        return HttpResponseRedirect(redirect_to='/fail')
    

#Login Authorization
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate email and password
        try:
            user = UserSignup.objects.get(email=email)
            if user.password == password:  # Compare plain-text passwords
                return Response(
                    {"message": "Login successful", "role": user.role},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Invalid password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except UserSignup.DoesNotExist:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
