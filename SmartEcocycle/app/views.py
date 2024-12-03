# signup/views.py
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserSignup
from .serializers import UserSignupSerializer
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.hashers import check_password

#homepage
def viewHomepage(request):
    return render(request, 'index.html')


#fail message
def fail(request):
    return render(request, 'fail.html')

def signup_form_page(request):
    return render(request, 'register.html')

#User Homepage 
def userHomepage(request):

    return render(request, 'user.html')

#Recycler Homepage 
def recyclerHomepage(request):
    return render(request, 'recycler.html')


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
                if user.role == 'user':
                    return HttpResponseRedirect(redirect_to='/user')
                else: return HttpResponseRedirect(redirect_to='/recycler')
            else:
                return HttpResponse('Invalid password')
        except UserSignup.DoesNotExist:
            return HttpResponse("User not found")
