# Create your models here.
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from enums import EnrollmentStatus

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
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Lessons(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Enrollment(models.Model):
    STATUS_CHOICES = [
        (status.value, status.name) for status in EnrollmentStatus
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completion_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=EnrollmentStatus.NOT_STARTED.value)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title} on {self.enrollment_date}"


admin.site.register(Profile)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(Course)
admin.site.register(Lessons)