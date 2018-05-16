from django.contrib import admin

# Register your models here.
from myevent.models import Event

admin.site.register(Event)
