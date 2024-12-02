# signup/views.py
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserSignup
from .serializers import UserSignupSerializer


#success message
def success(request):
    return render(request, 'success.html')


# This is the view that serves the form
def signup_form(request):
    if request.method == 'POST':
        # Get the form data from request.POST
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        center_name = request.POST.get('center_name', None)
        location = request.POST.get('location', None)
        contact = request.POST.get('contact', None)

        # Create a new user signup object
        user_signup = UserSignup(
            full_name=full_name,
            email=email,
            password=password,
            role=role,
            center_name=center_name,
            location=location,
            contact=contact
        )
        user_signup.save()

        # After saving the user, you can redirect to a success page or back to the form
        return redirect('signup-success')

    return render(request, 'register.html')

# If you want to handle the API endpoint using DRF
class UserSignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
