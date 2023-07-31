# Generated by Django 4.2 on 2023-07-28 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_userstory_image_remove_userstory_video_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstory',
            name='body',
        ),
        migrations.AddField(
            model_name='userstory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='userstory',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]