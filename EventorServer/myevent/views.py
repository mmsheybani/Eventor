from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView,RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from myevent.models import Event
from myevent.serializers import GetEventSerializers,CreateEventSerializer

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

class EventAPI(CreateAPIView, ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    def create(self, request, *args, **kwargs):
        serializer = CreateEventSerializer(data=request.data,context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetEventSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GetEventSerializers(queryset, many=True)
        return Response(serializer.data)


class GetEventApi(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = GetEventSerializers