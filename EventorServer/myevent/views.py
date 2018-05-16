from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse


class HelloWorld(APIView):

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            "mes":"sfasfsdf",
        })
