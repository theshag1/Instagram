from rest_framework import serializers

from .models import Spam_Story


class Kick_story_serializer(serializers.ModelSerializer):
    class Meta:
        model = Spam_Story
        fiedls = (

            'user',
            'releted',
            'date_time',
            'spam_type',
            'count'

        )
        read_only_fields = ('id')
