from django.contrib import admin

from .models import (
    Category,
    Choice,
    Course,
    Enrollment,
    Lesson,
    Notification,
    Order,
    Permission,
    Profile,
    Question,
    Quiz,
    Resource,
    Review,
    Role,
    Tag,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'field')
    search_fields = ('user__username', 'user__email', 'phone')
    filter_horizontal = ('roles',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('permissions',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'price', 'published', 'created_at')
    list_filter = ('published', 'categories', 'tags')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories', 'tags')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    ordering = ('course', 'order')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'completion_status', 'enrollment_date')
    list_filter = ('completion_status',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    list_filter = ('course',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'published')
    list_filter = ('published', 'course')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'order')
    list_filter = ('quiz',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'status', 'transaction_id', 'created_at')
    list_filter = ('status',)
    search_fields = ('transaction_id', 'user__username')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('rating',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'read', 'created_at')
    list_filter = ('read',)
