# Generated by Django 4.2 on 2023-07-25 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_remove_post_made_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archived_post', to='post.post')),
            ],
        ),
    ]
