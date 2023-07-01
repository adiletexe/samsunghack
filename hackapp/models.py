from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    photo = models.ImageField(upload_to='tasks', blank=True)
    weak = models.CharField(max_length=100, blank=True)


class Questions(models.Model):
    theme = models.CharField(max_length=100, blank=True)
    question = models.CharField(max_length=250, blank=True)


