# Generated by Django 4.2 on 2023-07-23 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_userstory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='see_user',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
