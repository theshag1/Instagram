# Generated by Django 4.2 on 2023-07-28 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_userstory_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='expiration_time',
            field=models.DateTimeField(db_index=True),
        ),
    ]
