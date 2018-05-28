from django.contrib import admin

# Register your models here.
from myevent.models import Event, Location

admin.site.register(Event)
admin.site.register(Location)

