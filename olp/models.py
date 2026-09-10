from django.conf import settings
from django.db import models

from .choices import EnrollmentStatus, OrderStatus


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField('Permission', blank=True, related_name='roles')

    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    phone = models.CharField(max_length=15)
    field = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    roles = models.ManyToManyField(Role, blank=True, related_name='profiles')

    def __str__(self):
        return self.user.get_username()

    @property
    def get_roles(self):
        return ', '.join(role.name for role in self.roles.all())


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='courses_taught',
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    categories = models.ManyToManyField(Category, blank=True, related_name='courses')
    tags = models.ManyToManyField(Tag, blank=True, related_name='courses')
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'order'],
                name='unique_lesson_order_per_course',
            ),
        ]

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completion_status = models.CharField(
        max_length=20,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.NOT_STARTED,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='unique_enrollment_per_user_course',
            ),
        ]

    def __str__(self):
        return (
            f'{self.user} enrolled in {self.course.title} '
            f'on {self.enrollment_date}'
        )


class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['quiz', 'order'],
                name='unique_question_order_per_quiz',
            ),
        ]

    def __str__(self):
        return self.text[:50]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='unique_review_per_user_course',
            ),
        ]

    def __str__(self):
        return f'Review by {self.user} for {self.course.title}'


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='orders')
    transaction_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    def __str__(self):
        return f'Order #{self.pk} - {self.user} - {self.course}'


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Notification for {self.user} - {self.created_at}'


# Keep the old name importable for any leftover references during migration rename.
Lessons = Lesson
