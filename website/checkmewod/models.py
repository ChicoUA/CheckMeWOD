from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.

class MyUser(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True, on_delete=models.CASCADE)

class VideoSubmission(models.Model):
    video_file = models.FileField

class Event(models.Model):
    name = models.CharField(max_length=50, null=False)
    start_Date = models.DateField(blank=False)
    end_Date = models.DateField()
    city = models.CharField(max_length=20)
    country = CountryField()
    price = models.CharField(max_length=10)
    short_Description = models.TextField()
    organizer = models.CharField(max_length=20)
    event_Logo = models.ImageField(null=True, blank=True)
