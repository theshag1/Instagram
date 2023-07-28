# Generated by Django 4.2 on 2023-07-28 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_userstoryarchived'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstory',
            name='image',
        ),
        migrations.RemoveField(
            model_name='userstory',
            name='video',
        ),
        migrations.AddField(
            model_name='userstory',
            name='body',
            field=models.FileField(default=('/media/photo_2023-07-28_13-42-25.jpg',), upload_to=''),
            preserve_default=False,
        ),
    ]
