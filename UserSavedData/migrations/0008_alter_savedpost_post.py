# Generated by Django 4.2 on 2023-08-11 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserSavedData', '0007_alter_savedpost_post_alter_savedpost_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedpost',
            name='post',
            field=models.CharField(max_length=123),
        ),
    ]