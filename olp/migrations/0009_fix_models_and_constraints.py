# Generated manually to align schema with fixed models

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def populate_order_fields(apps, schema_editor):
    Order = apps.get_model('olp', 'Order')
    Course = apps.get_model('olp', 'Course')
    User = apps.get_model(settings.AUTH_USER_MODEL)

    fallback_user = User.objects.order_by('id').first()
    fallback_course = Course.objects.order_by('id').first()

    for index, order in enumerate(Order.objects.all(), start=1):
        user_id = order.user_id or (fallback_user.id if fallback_user else None)
        course_id = order.course_id or (fallback_course.id if fallback_course else None)
        if user_id is None or course_id is None:
            order.delete()
            continue
        Order.objects.filter(pk=order.pk).update(
            user_id=user_id,
            course_id=course_id,
            transaction_id=order.transaction_id or f'migrated-{order.id}-{index}',
        )


class Migration(migrations.Migration):

    dependencies = [
        ('olp', '0008_order'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Lessons',
            new_name='Lesson',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, related_name='roles', to='olp.permission'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='roles',
            field=models.ManyToManyField(blank=True, related_name='profiles', to='olp.role'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='profile',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='course',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='courses', to='olp.category'),
        ),
        migrations.AddField(
            model_name='course',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='courses', to='olp.tag'),
        ),
        migrations.AddField(
            model_name='course',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='courses_taught',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['order']},
        ),
        migrations.AddConstraint(
            model_name='lesson',
            constraint=models.UniqueConstraint(
                fields=('course', 'order'),
                name='unique_lesson_order_per_course',
            ),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='completion_status',
            field=models.CharField(
                choices=[
                    ('NOT_STARTED', 'Not Started'),
                    ('IN_PROGRESS', 'In Progress'),
                    ('COMPLETED', 'Completed'),
                ],
                default='NOT_STARTED',
                max_length=20,
            ),
        ),
        migrations.AddConstraint(
            model_name='enrollment',
            constraint=models.UniqueConstraint(
                fields=('user', 'course'),
                name='unique_enrollment_per_user_course',
            ),
        ),
        migrations.AlterField(
            model_name='resource',
            name='course',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='resources',
                to='olp.course',
            ),
        ),
        migrations.AlterField(
            model_name='resource',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='quizzes',
                to='olp.course',
            ),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='questions',
                to='olp.quiz',
            ),
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['order']},
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.UniqueConstraint(
                fields=('quiz', 'order'),
                name='unique_question_order_per_quiz',
            ),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='choices',
                to='olp.question',
            ),
        ),
        migrations.AlterField(
            model_name='choice',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='course',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='reviews',
                to='olp.course',
            ),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='reviews',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(
                fields=('user', 'course'),
                name='unique_review_per_user_course',
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='orders',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='course',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders',
                to='olp.course',
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.RunPython(populate_order_fields, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[
                    ('PENDING', 'Pending'),
                    ('COMPLETED', 'Completed'),
                    ('FAILED', 'Failed'),
                ],
                default='PENDING',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='orders',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='order',
            name='course',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders',
                to='olp.course',
            ),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='notifications',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
