# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', viewHomepage.as_view(), name='homepage'),
    path('signup/', SignUpPageView.as_view(), name='signup'),
    path('api/signup/', SignUpView.as_view(), name='signup-api'),
]
