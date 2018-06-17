from django.db import models

from myuser.models import User as myuser, User


# Create your models here.


class Subject(models.Model):
    title = models.CharField(max_length=50, null=False)


class Location(models.Model):
    address = models.CharField(max_length=200, null=False)
    lat = models.FloatField()
    long = models.FloatField()
    capacity = models.IntegerField()


class Event(models.Model):
    title = models.CharField(max_length=100, null=False)
    date = models.DateTimeField(null=False)
    description = models.CharField(max_length=500)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING,null=False)
    subject = models.ManyToManyField(Subject, through='SubjectRelation')
    holder=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False)
    header_image=models.CharField(max_length=100,default="")


class Ticket(models.Model):
    price = models.IntegerField(null=False)
    count = models.IntegerField(null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False)


class DiscountCode(models.Model):
    percent = models.FloatField(null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    expiration = models.DateTimeField(null=False)


class SubjectRelation(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Participate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    participant = models.ForeignKey(myuser, on_delete=models.DO_NOTHING)


class HeaderImage(models.Model):
    url = models.CharField(max_length=100, null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False)
