from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer
from django.views import View

# Create your views here.

class viewHomepage(View):
    def get(self, request):
        return render(request, 'index.html')


class SignUpPageView(View):
    def get(self, request):
        return render(request, 'signup.html')


class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            
            # Here you can create the user or perform other actions
            # For example, save the user:
            # user = User.objects.create(
            #     name=serializer.validated_data['name'],
            #     email=serializer.validated_data['email'],
            #     phone=serializer.validated_data['phone'],
            #     password=serializer.validated_data['password']
            # )
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        print(serializer)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


