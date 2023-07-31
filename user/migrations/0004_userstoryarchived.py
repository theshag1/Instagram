# Generated by Django 4.2 on 2023-07-28 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_userstory_expiration_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStoryArchived',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('video', models.FileField(blank=True, null=True, upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_story_archived', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]