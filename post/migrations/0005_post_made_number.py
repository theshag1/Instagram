# Generated by Django 4.2 on 2023-07-24 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_remove_like_like_remove_post_caption_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='made_number',
            field=models.CharField(auto_created='2L!2', default='AsDf'),
            preserve_default=False,
        ),
    ]