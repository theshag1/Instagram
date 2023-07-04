from django.db import models


# Create your models here.
class Follow(models.Model):
    follow = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='follow_user')
    followed_user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='follower_user')

