# signup/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_form, name='user-signup'),  # Handle form submission via POST
    path('signup-success/', views.success, name='signup-success'),  # Success page after signup
]
