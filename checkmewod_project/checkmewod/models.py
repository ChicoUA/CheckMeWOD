from django.db import models
from django.contrib.auth.models import User, Group
from django_countries.fields import CountryField
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear

# Create your models here.


class VideoSubmission(models.Model):
    video_id = models.TextField(null=True)
    video_file = models.FileField(upload_to='checkmewod/static/uploaded_files/', null=True, verbose_name="")
    exercise_in_video = models.TextField(null=True)
    number_reps = models.TextField(null=True)
    number_correct_reps = models.TextField(null=True)
    number_incorrect_reps = models.TextField(null=True)
    video_status = models.TextField(null=True)
    user_email = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    frames_per_rep = models.TextField(null=True)

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
    