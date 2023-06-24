from uuid import uuid5
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    sharif = models.CharField(max_length=100)
    super = models.CharField(max_length=100)
    dekanat = models.CharField(max_length=100)
    talaba = models.CharField(max_length=100)

class Foydalanuvchi(models.Model):
    token = models.UUIDField(unique=uuid5)
    