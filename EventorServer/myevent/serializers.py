from rest_framework import serializers
from myevent.models import Event

class EventSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'date', 'description', 'location', 'subject','id')
