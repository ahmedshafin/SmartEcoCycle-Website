# signup/views.py
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserSignup
from .serializers import UserSignupSerializer
from django.http import HttpResponseRedirect

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
