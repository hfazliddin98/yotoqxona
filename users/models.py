from uuid import uuid5
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    sharif = models.CharField(max_length=100)
    super = models.CharField(max_length=100, blank=True)
    dekanat = models.CharField(max_length=100, blank=True)
    fakultet = models.CharField(max_length=100, blank=True)
    talaba = models.CharField(max_length=100, blank=True)
    parol = models.CharField(max_length=100)

    