from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MyUser(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True, on_delete=models.CASCADE)

class VideoSubmission(models.Model):
    video_file = models.FileField