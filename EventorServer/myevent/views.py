from os.path import join

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from EventorServer import settings
from myevent import Backtory
from myevent.models import Event, Location
from myevent.serializers import GetEventSerializers, CreateEventSerializer, LocationSerializer

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import requests


class EventAPI(CreateAPIView, ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = CreateEventSerializer

    def create(self, request, *args, **kwargs):
        saved_file_url=""
        if request.FILES['image']:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            saved_file_url=Backtory.upload_file(open(join(settings.MEDIA_ROOT,filename), 'rb'))

        instance = Event()
        serializer = CreateEventSerializer(instance, data=request.data, context={'user': request.user,'image':saved_file_url})
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        s = serializer.create(serializer.validated_data)
        ss = GetEventSerializers(instance=s)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(ss.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetEventSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GetEventSerializers(queryset, many=True)
        return Response(serializer.data)


class GetEventApi(RetrieveAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = GetEventSerializers


class LocationApi(CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class test(CreateAPIView):

    def post(self, request, *args, **kwargs):
        if request.FILES['image']:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            fi=open(join(settings.MEDIA_ROOT,filename), 'rb')
            saved_file_url=Backtory.upload_file(open(join(settings.MEDIA_ROOT,filename), 'rb'))
            return Response({
                'saved_file_url':saved_file_url
            },status=status.HTTP_200_OK)


