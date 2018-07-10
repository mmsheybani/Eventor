from rest_framework import serializers

from myuser.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    # username=serializers.CharField(required=True)
    # first_name=serializers.CharField(required=True)
    # last_name=serializers.CharField(required=True)
    # email=serializers.CharField(required=True)
    # profile_picture = serializers.CharField(required=False)
    # password=serializers.CharField(required=True,write_only=True)
    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password','phone_number')
    def create(self, validated_data):
        validated_data['profile_picture']=self.context.get('profile_picture')
        user=User.objects.create(**validated_data)
        return user


class GetUserSerializer(serializers.ModelSerializer):
    # username=serializers.CharField(required=True)
    # first_name=serializers.CharField(required=True)
    # last_name=serializers.CharField(required=True)
    # email=serializers.CharField(required=True)
    # profile_picture = serializers.CharField(required=False)
    # password=serializers.CharField(required=True,write_only=True)
    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password','phone_number','profile_picture')
    def create(self, validated_data):
        validated_data['profile_picture']=self.context.get('profile_picture')
        user=User.objects.create(**validated_data)
        return user
