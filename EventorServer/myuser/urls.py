from django.contrib import admin
from django.urls import path, include
from .views import SignUp, Login

urlpatterns=[
    path('signup/', SignUp.as_view()),
    path('login/',Login.as_view()),
]