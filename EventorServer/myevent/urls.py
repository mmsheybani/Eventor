from django.urls import path, include

from myevent.views import EventApi

urlpatterns = [
    path('aa/<int:pk>', EventApi.as_view()),
]