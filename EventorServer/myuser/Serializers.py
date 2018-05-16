from rest_framework import serializers

from myuser.models import User


class UserSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    email=serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    profile_picture = serializers.CharField(required=False)
    password=serializers.CharField(required=True)
    def create(self, validated_data):
        user=User.objects.create(**validated_data)
        return user

