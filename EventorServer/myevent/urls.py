from django.urls import path, include

from myevent.views import GetEventApi, EventAPI, LocationApi, test

urlpatterns = [
    # path('', GetEventListApi.as_view()),
    path('<int:pk>', GetEventApi.as_view()),
    path('', EventAPI.as_view()),
    path('location/', LocationApi.as_view()),

]
