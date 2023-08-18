# Generated by Django 4.2 on 2023-08-08 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserSavedData', '0002_userpostsaved_savedpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedpost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_saved_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
