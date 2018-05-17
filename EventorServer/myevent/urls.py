from django.urls import path, include

from myevent.views import EventApi, EventListApi

urlpatterns = [
    path('<int:pk>', EventApi.as_view()),
    path('list', EventListApi.as_view()),

]