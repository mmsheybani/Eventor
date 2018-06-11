from django.contrib import admin

# Register your models here.
from myevent.models import Event, Location, Ticket

admin.site.register(Event)
admin.site.register(Location)
admin.site.register(Ticket)

