from rest_framework import serializers
from myevent.models import Event, Location
from myuser.Serializers import UserSerializer
from myuser.models import User


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields=('id','address','lat','long','capacity')
class GetEventSerializers(serializers.ModelSerializer):
    location=LocationSerializer(many=False,read_only=True)
    holder=UserSerializer(many=False,read_only=True)
    class Meta:
        model = Event
        fields = ('title', 'date', 'description', 'location', 'subject','id','holder')
class CreateEventSerializer(serializers.ModelSerializer):
    location=serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(),many=False)
    holder=serializers.SerializerMethodField(source="get_holder")
    def get_holder(self,obj):
        print(1)
        user=self.context.get('user')
        return user
    class Meta:
        model = Event
        fields = ('title', 'date', 'description', 'location', 'subject','id','holder')
