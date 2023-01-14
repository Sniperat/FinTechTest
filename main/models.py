from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    documentCode = models.CharField(max_length=9, null=True, blank=True)
    documentDate = models.DateField(null=True, blank=True)


class CardModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    expire = models.CharField(max_length=4)
    title = models.CharField(max_length=20, null=True, blank=True)
    cvv = models.CharField(max_length=5, null=True, blank=True)
    active = models.BooleanField(default=False)


class OrderHistoryModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    price = models.IntegerField(default=0)
    location = models.CharField(max_length=255)
    market = models.CharField(max_length=255)