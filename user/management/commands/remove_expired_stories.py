from django.core.management.base import BaseCommand
from django.db.models.functions import Now

from user.models import UserStory


class Command(BaseCommand):
    help = 'Remove expried  story'

    def handle(self, *args, **options):
        UserStory._base_manager.filter(expiration_time__gte=Now()).delete()
