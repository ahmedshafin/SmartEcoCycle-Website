# signup/views.py
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

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
    if not request.session.get('is_authenticated'):  # Check session authentication
        return redirect('homepage')  # Redirect to login page if not authenticated
    return render(request, 'user.html')

#Recycler Homepage 
def recyclerHomepage(request):
    if not request.session.get('is_authenticated'):  # Check session authentication
        return redirect('homepage')
    pickup = PickupRequest.objects.filter()
    pickup_count= len(pickup)
    recycler = Recycler.objects.filter()
    available_recycler= len(recycler)
    
    
    args = {
        "pickup": pickup,
        "pickup_count": pickup_count,
        "available_recycler": available_recycler,
        
    }
    return render(request, 'recycler.html',args)


# Signup
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

        try:
            user = UserSignup.objects.get(email=email)

            # Secure password comparison
            if user.password == password:
                # Set session
                request.session['is_authenticated'] = True
                request.session['user_role'] = user.role

                if user.role == 'user':
                    return HttpResponseRedirect(redirect_to='/user')
                elif user.role == 'recycle-center':
                    return HttpResponseRedirect(redirect_to='/recycler')
                else:
                    return HttpResponseRedirect(redirect_to='/superAdmin')
            else:
                return HttpResponse('Invalid password')
        except UserSignup.DoesNotExist:
            return HttpResponse("User not found")

    def get(self, request):
        # Render the login page
        return render(request, 'index.html')
        

#Contact Us
class contactUs(APIView):
    def post(self, request):
        
        serializer = contactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(redirect_to='/')
        
        return HttpResponseRedirect(redirect_to='/fail')
    
#Contact Us render
def contactUsView(request):
    return render(request, 'contact.html')

#Logout
def logout(request):
    request.session.flush()  # Clear all session data
    return redirect('homepage')


#Super Admin
def superAdmin(request):
    if not request.session.get('is_authenticated'):  # Check session authentication
        return redirect('homepage')  # Redirect to login page if not authenticated
    return render(request, 'admin.html')
    


#App signup

class AppSignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AppLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = UserSignup.objects.get(email=email)

            # Secure password comparison (replace with hashed password check)
            if user.password == password:
                # Return user role and success message
                return Response({
                    'message': 'Login successful',
                    'role': user.role,
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        except UserSignup.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

class PickupRequestView(APIView):
    def post(self, request):
        serializer = PickupRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Pickup request created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PickupRequestCreateView(generics.CreateAPIView):
    queryset = PickupRequest.objects.all()
    serializer_class = PickupRequestSerializer


class ContactUsAPIView(APIView):
    def post(self, request, format=None):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your message has been sent successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#GPS Tracking
def map(request, slug):
    map_obj = get_object_or_404(PickupRequest, id=slug)
    latitude = map_obj.latitude
    longitude = map_obj.longitude
    google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"

    return redirect(google_maps_url)


#Recycler
def add_recycler(request):
    recycler = Recycler.objects.filter()
    
    
    
    args = {
        "recycler": recycler,
        

           
    }

    return render(request, "addRecycler.html",args)


@api_view(['GET', 'POST'])
@csrf_exempt
def recycler_list_create(request):
    if request.method == 'GET':
        recyclers = Recycler.objects.all()
        serializer = RecyclerSerializer(recyclers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecyclerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def recycler_detail(request, pk):
    try:
        recycler = Recycler.objects.get(pk=pk)
    except Recycler.DoesNotExist:
        return Response({"error": "Recycler not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecyclerSerializer(recycler)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = RecyclerSerializer(recycler, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        recycler.delete()
        return Response({"message": "Recycler deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    



