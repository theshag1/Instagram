# Generated by Django 4.2 on 2023-08-11 18:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0015_alter_updatecode_data_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updatecode',
            name='data_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 11, 22, 31, 21, 776149)),
        ),
    ]
