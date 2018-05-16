from django.contrib import admin
from django.urls import path, include
from myevent.views import HelloWorld

urlpatterns=[
    path('signup/', HelloWorld.as_view(), name='helloWorld')
]