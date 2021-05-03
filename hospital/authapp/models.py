from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime
# Create your models here.


class Constants:
    # Class for various choices on the enumerations

    STATUS = (
        ('SampleCollected', 'SampleColected'),
        ('TestingUnderProcess', 'TestingUnderProcess'),
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
    )

class UserRegistrationModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    aadhar_number = models.CharField(max_length=16)


class SampleCollection(models.Model):
    sampleid = models.CharField(max_length=10)
    age = models.IntegerField()
    date = models.DateField()
    fever = models.BooleanField(default=False)
    drycough = models.BooleanField(default=False)
    tiredness = models.BooleanField(default=False)
    difficultybreathing = models.BooleanField(default=False)
    chestpain = models.BooleanField(default=False)
    lossofspeech = models.BooleanField(default=False)


class SampleStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sampleid = models.CharField(max_length=10)
    status = models.CharField(max_length=30, choices=Constants.STATUS, default='SampleCollected')