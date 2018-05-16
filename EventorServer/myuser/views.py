from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from myuser.Serializers import UserSerializer
from myuser.models import User


class SignUp(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=UserSerializer(data=request.data)
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
                'token' : token.key
            })
        return Response("nok")
