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
        fields = ('id','title', 'date', 'description', 'location', 'subject','holder','header_image')
class CreateEventSerializer(serializers.ModelSerializer):
    location=serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(),many=False)
    #holder=serializers.SerializerMethodField(source="get_holder")
    class Meta:
        model = Event
        fields = ('id','title', 'date', 'description', 'location', 'subject')
    def create(self, validated_data):
        # name = validated_data['name']
        validated_data['holder']=self.context.get('user')
        validated_data['header_image']=self.context.get('image')
        event = Event.objects.create(**validated_data)
        return event
