# signals.py

from django.dispatch import Signal
from django.dispatch import receiver
from django.utils.timezone import now
from .models import User

story_deleted = Signal()


@receiver(story_deleted, sender=User)
def delete_story(sender, instance, **kwargs):
    if instance.story and (now() - instance.story.created).seconds >= 1800:
        instance.story.delete()
