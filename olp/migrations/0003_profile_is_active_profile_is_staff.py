# Generated by Django 5.0.3 on 2024-04-25 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olp', '0002_permission_role_profile_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]