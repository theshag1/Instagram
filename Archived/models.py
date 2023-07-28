from django.db import models


# Create your models here.

class UserStoryArchived(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user_story_archived')
    image = models.ImageField(blank=True, null=True)
    video = models.FileField(blank=True, null=True)


