from os.path import join

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from EventorServer import settings
from myevent import Backtory
from myuser.Serializers import UserSerializer
from myuser.models import User


class SignUp(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        saved_file_url = ""
        if request.FILES['profile_picture']:
            myfile = request.FILES['profile_picture']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            saved_file_url = Backtory.upload_file(open(join(settings.MEDIA_ROOT, filename), 'rb'))
            fs.delete(filename)
        print(saved_file_url)
        print(request.data)
        serializer=UserSerializer(data=request.data,context={'profile_picture':saved_file_url})
        serializer.is_valid(raise_exception=True)
        user=serializer.create(serializer.data)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token' : token.key
        })

class Login(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        user=User.objects.filter(username=username).filter(password=password).first()
        if(user!=None):
            token=Token.objects.filter(user=user).first()
            return Response({
                'token' : token.key,
                'time' : user.date_joined
            })
        return Response("nok")
