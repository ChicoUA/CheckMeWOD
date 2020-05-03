from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear

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
    event_URL = models.URLField(null=False, default='')
    event_Logo = models.ImageField(upload_to = 'images/event_logos/', null=True, blank=True)

    def extract(self, element, date=start_Date):
        if element == 'day':
            return ExtractDay(date)
        elif element == 'month':
            return ExtractMonth(date)
        elif element == 'year':
            return ExtractYear(date)
