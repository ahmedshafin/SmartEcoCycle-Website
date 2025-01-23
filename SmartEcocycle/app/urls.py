# signup/urls.py
from django.urls import path
from . import views 
from .views import *

urlpatterns = [
    path('', views.viewHomepage, name='homepage'),
    path('fail/', views.fail, name='fail'),  # fail page after signup
    path('api/signup/', UserSignupView.as_view(), name='user-signup'),
    path('signup/', signup_form_page, name='signup-form'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('user/', views.userHomepage, name='user'),
    path('recycler/', views.recyclerHomepage, name='recycler'),
    path('contact/',views.contactUs.as_view(), name='contact'),
    path('contactUs/',views.contactUsView, name='contactUs'),
    path('logout/',views.logout, name='logout'),
]
