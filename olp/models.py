
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    field = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
admin.site.register(Profile)