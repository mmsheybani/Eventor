from json import JSONDecoder
from os.path import join
from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from EventorServer import settings
from myevent import Backtory
from myevent.models import Event, Location, Ticket
from myevent.serializers import GetEventSerializers, CreateEventSerializer, LocationSerializer, CreateTicketSerializers, \
    GetTicketSerializers
from rest_framework.response import Response
from myevent.serializers import GetEventSerializers, CreateEventSerializer, LocationSerializer, CreateTicketSerializers, \
    GetTicketSerializers


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if (request.method in ['GET'] or (request.user and request.user.is_authenticated)):
            return True
        return False


class EventAPI(CreateAPIView, ListAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = Event.objects.all()
    serializer_class = CreateEventSerializer

    def create(self, request, *args, **kwargs):
        saved_file_url=""
        print(request.data)
        print(request.POST)
        print(request.FILES)
        print(request.data.get('files'))
        if request.FILES.get('header_image'):
            print(1)
            myfile = request.FILES.get('header_image')
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            saved_file_url=Backtory.upload_file(open(join(settings.MEDIA_ROOT,filename), 'rb'))
            print(2)
            fs.delete(filename)

        instance = Event()
        serializer = CreateEventSerializer(instance, data=request.data, context={'user': request.user,'image':saved_file_url})
        serializer.is_valid(raise_exception=True)
        s = serializer.create(serializer.validated_data)
        ss = GetEventSerializers(instance=s)
        return Response(ss.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetEventSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GetEventSerializers(queryset, many=True)
        return Response(serializer.data)
class GetEventApi(RetrieveAPIView,UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = Event.objects.all()
    serializer_class = GetEventSerializers
    def update(self, request, *args, **kwargs):
        isAuth=IsAuthenticated()
        if isAuth.has_permission(request,self):
            if request.user == Event.objects.filter(id=kwargs.get("pk")).first().holder:
                saved_file_url = ""
                # print(request.data)
                # json = request.data.get('user')
                # print(str(json))
                # jsonDecoder = JSONDecoder()
                # json = jsonDecoder.decode(json)
                # print(json)
                # image = request.data.get('file')
                if request.FILES.get("header_image"):
                    myfile = request.FILES['header_image']
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name, myfile)
                    saved_file_url = Backtory.upload_file(open(join(settings.MEDIA_ROOT, filename), 'rb'))
                    fs.delete(filename)
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = CreateEventSerializer(instance, data=request.data, partial=partial,context={"image":saved_file_url})
                serializer.is_valid(raise_exception=True)
                s=serializer.save(header_image=saved_file_url)
                if getattr(instance, '_prefetched_objects_cache', None):
                    instance._prefetched_objects_cache = {}

                return Response(GetEventSerializers(instance=s).data)
            return Response("Access Denied")
        return Response("not authorized")


class LocationApi(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class TicketApi(CreateAPIView, ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ticket.objects.all()
    serializer_class = CreateTicketSerializers

    def create(self, request, *args, **kwargs):
        instance = Ticket()
        serializer = CreateTicketSerializers(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        s = serializer.create(serializer.validated_data)
        ss = GetTicketSerializers(instance=s)
        return Response(ss.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetTicketSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GetTicketSerializers(queryset, many=True)
        return Response(serializer.data)



class Get_holder_events(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        holder = request.user
        events = Event.objects.filter(holder=holder)
        serializer = GetEventSerializers(events, many=True)
        return Response(serializer.data)
