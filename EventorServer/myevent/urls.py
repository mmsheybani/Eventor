from django.urls import path, include

from myevent.views import GetEventApi, EventAPI, LocationApi

from myevent.views import TicketApi

urlpatterns = [
    # path('', GetEventListApi.as_view()),
    path('<int:pk>', GetEventApi.as_view()),
    path('', EventAPI.as_view()),
    path('location/', LocationApi.as_view()),
    path('Ticket/', TicketApi.as_view()),

]
