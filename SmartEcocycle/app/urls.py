from django.urls import path
from . import views 
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.viewHomepage, name='homepage'),
    path('fail/', views.fail, name='fail'),  # fail page after signup
    path('api/signup/', UserSignupView.as_view(), name='user-signup'),
    path('app/signup/', AppSignupView.as_view(), name='app-signup'),
    path('signup/', signup_form_page, name='signup-form'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('user/', views.userHomepage, name='user'),
    path('recycler/', views.recyclerHomepage, name='recycler'),
    path('contact/',views.contactUs.as_view(), name='contact'),
    path('contactUs/',views.contactUsView, name='contactUs'),
    path('logout/',views.logout, name='logout'),
    path('superAdmin/',views.superAdmin, name='superAdmin'),
    path('app/login/', AppLoginView.as_view(), name='applogin'),
    path('app/pickup-requests/', PickupRequestCreateView.as_view(), name='pickup-request-create'),
    path('api/contact/', ContactUsAPIView.as_view(), name='contact-us'),
    path('map/<int:slug>', views.map, name= 'map'),
    path('resolve/<int:slug>', views.resolve, name='resolve'),
    path('api/recycler/login/', recycler_login, name='recycler_login'),
    path('recyclers/', views.recycler_list, name='recycler-list'),
    path('recyclers/<int:pk>/', views.recycler_detail, name='recycler-detail'),
    path('create/recycler/', views.createRecycler, name='createRecycler'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/pickup-requests/', PickupRequestView.as_view(), name='pickup-requests'),
    path('api/pickup-requests/<int:pk>/update-status/', UpdatePickupStatusView.as_view(), name='update-status'),
    path('displayContact/', views.displayContactView, name = "displayContact"),
    path('deleteContact/<int:slug>', views.deleteContact, name = "deleteContact"),


]
