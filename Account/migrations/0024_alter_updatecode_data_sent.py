# Generated by Django 4.2 on 2023-07-26 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0023_alter_updatecode_data_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updatecode',
            name='data_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 26, 16, 11, 8, 82832)),
        ),
    ]