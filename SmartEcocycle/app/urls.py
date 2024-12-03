# signup/urls.py
from django.urls import path
from . import views 
from .views import UserSignupView, signup_form_page,LoginView

urlpatterns = [
    path('', views.viewHomepage, name='homepage'),
   # path('signup/', views.signup_form, name='user-signup'),  # Handle form submission via POST
    path('fail/', views.fail, name='fail'),  # Success page after signup
    path('api/signup/', UserSignupView.as_view(), name='user-signup'),
    path('signup/', signup_form_page, name='signup-form'),
    path('api/login/', LoginView.as_view(), name='login'),
]
