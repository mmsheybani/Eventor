from django.contrib import admin

# Register your models here.
from myuser.models import User

admin.site.register(User)
