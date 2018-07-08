from os.path import join

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView

from EventorServer import settings
from myevent import Backtory
from myuser.Serializers import CreateUserSerializer, GetUserSerializer
from myuser.models import User

# from EventorServer.myevent.models import Event


class SignUp(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        saved_file_url = ""
        if request.FILES.get('profile_picture'):
            myfile = request.FILES['profile_picture']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            saved_file_url = Backtory.upload_file(open(join(settings.MEDIA_ROOT, filename), 'rb'))
            fs.delete(filename)
        print(saved_file_url)
        print(request.data)
        serializer=CreateUserSerializer(data=request.data, context={'profile_picture':saved_file_url})
        serializer.is_valid(raise_exception=True)
        user=serializer.create(serializer.data)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token' : token.key,
            'user': serializer.data
        })

class Login(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        user=User.objects.filter(username=username).filter(password=password).first()
        if(user!=None):
            token =Token.objects.get_or_create(user=user)[0]
            serializer=GetUserSerializer(instance=user)
            return Response({
                'token' : token.key,
                'time' : user.date_joined,
                'user': serializer.data
            })
        return Response("nok")

class update(UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    def update(self, request, *args, **kwargs):
        print(kwargs.get("pk"))
        if request.user == User.objects.filter(phone_number=(kwargs.get("pk"))).first():
            saved_file_url = ""
            # print(request.data)
            # json = request.data.get('user')
            # print(str(json))
            # jsonDecoder = JSONDecoder()
            # json = jsonDecoder.decode(json)
            # print(json)
            # image = request.data.get('file')
            if request.FILES.get("profile_picture"):
                myfile = request.FILES['profile_picture']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                saved_file_url = Backtory.upload_file(open(join(settings.MEDIA_ROOT, filename), 'rb'))
                fs.delete(filename)
            partial = kwargs.pop('partial', False)
            instance = self.get_object()

            serializer = CreateUserSerializer(instance, data=request.data, partial=partial, context={"profile_picture": saved_file_url})
            serializer.is_valid(raise_exception=True)
            s = serializer.save(profile_picture=saved_file_url)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(GetUserSerializer(instance=s).data)
        return Response("Access Denied")

