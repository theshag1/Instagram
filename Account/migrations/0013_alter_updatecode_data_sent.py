# Generated by Django 4.2 on 2023-07-23 18:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0012_alter_updatecode_data_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updatecode',
            name='data_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 23, 22, 10, 0, 96676)),
        ),
    ]
