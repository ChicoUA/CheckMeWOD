from django.db import models
from django.contrib.auth.models import User, Group

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

class Events(models.Model):
    name = models.TextField(null=True)
    start_date = models.TextField(null=True)
    end_date = models.TextField(null=True)
    start_time = models.TextField(null=True)
    end_time = models.TextField(null=True)
    registration_url = models.TextField(null=True)
    website_url = models.TextField(null=True)
    country = models.TextField(null=True)
    location = models.TextField(null=True)
    street = models.TextField(null=True)
    zipcode = models.TextField(null=True)
    price = models.TextField(null=True)
    description = models.TextField(null=True)
    