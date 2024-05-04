# Create your models here.
from enum import Enum
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from .enums import EnrollmentStatus, OrderStatus


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
class EnrollmentStatus(Enum):
    NOT_STARTED = 'Not Started'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
class Enrollment(models.Model):
    """
    An enrollment represents a user's registration for a course.

    Attributes:
        user (ForeignKey): The user who is enrolled in the course.
        course (ForeignKey): The course the user is enrolled in.
        enrollment_date (DateTimeField): The date and time the user enrolled in the course.
        completion_status (CharField): The status of the user's completion of the course.
    """
    STATUS_CHOICES = [
        (EnrollmentStatus.NOT_STARTED.name, 'Not Started'),
        (EnrollmentStatus.IN_PROGRESS.name, 'In Progress'),
        (EnrollmentStatus.COMPLETED.name, 'Completed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completion_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=EnrollmentStatus.NOT_STARTED.value)

    def __str__(self):
        """
        Returns a string representing the user's enrollment in the course.
        """
        return f"{self.user.username} enrolled in {self.course.title} on {self.enrollment_date}"




class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.text[:50]  # Return first 50 characters of the question text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text
    
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.course.title}"

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders'),
    course = models.ForeignKey(Course, on_delete=models.CASCADE),
    transaction_id = models.CharField(max_length=255),
    created_at = models.DateTimeField(auto_now_add=True),
    status = models.CharField(max_length=20)
    
admin.site.register(Profile)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(Course)
admin.site.register(Lessons)
admin.site.register(Enrollment)
admin.site.register(Resource)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Review)