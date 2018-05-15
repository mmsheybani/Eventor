from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone_number=models.CharField(max_length=11,primary_key=True)
    profile_picture=models.CharField(max_length=100)
    token=models.CharField(max_length=100,unique=True)
    expire_date_token=models.DateTimeField()

