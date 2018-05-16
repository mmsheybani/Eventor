from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from myevent.models import Event
from myevent.serializers import EventSerilizers

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

class EventApi(CreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerilizers

