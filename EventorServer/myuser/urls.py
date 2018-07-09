from django.contrib import admin
from django.urls import path, include
from .views import SignUp, Login, UserApi

urlpatterns=[
    path('signup/', SignUp.as_view()),
    path('login/',Login.as_view()),
    path('<slug:pk>',UserApi.as_view()),
    path('', UserApi.as_view()),

]