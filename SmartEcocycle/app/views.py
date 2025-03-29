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
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.permissions import AllowAny


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
    recycler = RecyclerCreate.objects.filter()
    available_recycler= len(recycler)
    
    
    args = {
        "pickup": pickup,
        "pickup_count": pickup_count,
        "available_recycler": available_recycler,
        "recycler": recycler, 
        
    }
    return render(request, 'recycler.html',args)


# Signup
class UserSignupView(APIView):
    permission_classes = [AllowAny]  # This allows anyone to access this view
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
    permission_classes = [AllowAny]  # This allows anyone to access this view
    def post(self, request):
        
        email = request.data.get('email')
        password = request.data.get('password')
        

        try:
            user = UserSignup.objects.get(email=email)

            # Secure password comparison
            if check_password(password,user.password):
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
    permission_classes = [AllowAny]
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
    authentication_classes = []  # No authentication required
    permission_classes = []      # No permissions required

    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Creates the user with hashed password
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#App login

class AppLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'message': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UserSignup.objects.get(email=email)
            # Assuming passwords are hashed; if not, update signup to hash them
            if check_password(password, user.password):  # Use hashed password check
                refresh = RefreshToken.for_user(user)
                
                
                return Response({
                    'message': 'Login successful',
                    'role': user.role,
                    'full_name': user.full_name,
                    'rating': user.rating,
                    'total_pickup': user.total_pickup,
                    'total_recycled': user.total_recycled,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'message': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except UserSignup.DoesNotExist:
            return Response(
                {'message': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        


class PickupRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def post(self, request):
        increment = UserSignup.objects.get(email = request.user)
        increment.total_pickup += 1  # Properly increment the field
        print(request.data)
        quantity = int(request.data.get("quantity", 0))  # Default to 0 if key is missing
        
        increment.total_recycled += quantity
        increment.save()  # Save the changes to the database
        
        with transaction.atomic():  # Ensure consistency
            
            serializer = PickupRequestSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    def get(self, request):
        
        requests = PickupRequest.objects.filter(user=request.user).order_by('-created_at')
        serializer = PickupRequestSerializer(requests, many=True)
        return Response(serializer.data)
    

class UpdatePickupStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            pickup = PickupRequest.objects.get(pk=pk, user=request.user)
            new_status = request.data.get('status')
            if new_status not in dict(PickupRequest.STATUS_CHOICES).keys():
                return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
            pickup.status = new_status
            pickup.save()
            serializer = PickupRequestSerializer(pickup)
            return Response(serializer.data)
        except PickupRequest.DoesNotExist:
            return Response({'error': 'Pickup request not found'}, status=status.HTTP_404_NOT_FOUND)


class PickupRequestCreateView(generics.CreateAPIView):
    queryset = PickupRequest.objects.all()
    serializer_class = PickupRequestSerializer


class ContactUsAPIView(APIView):
    permission_classes = []
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



#assigning the work to the teams
def resolve(request, slug):
    delReport = PickupRequest.objects.get(id=slug)
    
    if request.method == 'POST':
        delReport.status = 'Assigned'
        delReport.save()
        teamName = request.POST.get('teamName')
        status = 'Inactive'
        teams = assigned_recycler(name=teamName, status=status, address=delReport.address,quantity=
                             delReport.quantity,latitude=delReport.latitude,longitude=delReport.longitude)
        try:
            recycler = RecyclerCreate.objects.get(name=teamName)
            recycler.status = 'Inactive'  # Update status
            recycler.save()
        except RecyclerCreate.DoesNotExist:
            return HttpResponse("Recycler not found", status=404)

        teams.save()
    
    
    
    return redirect('recycler')



# Recycler Login API View
@api_view(['POST'])
@permission_classes([AllowAny])
def recycler_login(request):

    serializer = RecyclerLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        
        contact_number = serializer.validated_data['contact_number']
        password = serializer.validated_data['password']
        
        try:
            recycler = RecyclerCreate.objects.get(contact_number=contact_number)
            if recycler.password == password:  # Simple password check
                
                return Response({
                    "message": "Login successful",
                    "recycler_id": recycler.id,
                    "name": recycler.name,
                    "status": recycler.status,
                    "assigned_area": recycler.assigned_area,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except RecyclerCreate.DoesNotExist:
            return Response({"error": "Recycler not found"}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow anyone to access this endpoint
def recycler_list(request):
    
    if request.method == 'GET':
        recyclers = RecyclerCreate.objects.all()
        serializer = RecyclerSerializerCreate(recyclers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecyclerSerializerCreate(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  # Allow anyone to access this endpoint
def recycler_detail(request, pk):
     
    recycler = get_object_or_404(RecyclerCreate, pk=pk)

    if request.method == 'GET':
        serializer = RecyclerSerializerCreate(recycler)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RecyclerSerializerCreate(recycler, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        recycler.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

def createRecycler(request):
    if not request.session.get('is_authenticated'):  # Check session authentication
        return redirect('homepage')
    return render(request, 'createRecycler.html')






    



