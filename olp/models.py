# Create your models here.
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from Online_Learning_Platform import settings


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    field = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    roles = models.ManyToManyField(Role, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    @property
    def get_roles(self):
        return ", ".join([role.name for role in self.roles.all()])

admin.site.register(Profile)
admin.site.register(Permission)
admin.site.register(Role)