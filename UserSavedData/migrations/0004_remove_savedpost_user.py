# Generated by Django 4.2 on 2023-08-11 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserSavedData', '0003_alter_savedpost_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedpost',
            name='user',
        ),
    ]
