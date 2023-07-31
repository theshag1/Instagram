from rest_framework import serializers

from Archived.models import UserStoryArchived


class ArchivedStorySerizlier(serializers.ModelSerializer):
    class Meta:
        model = UserStoryArchived
        fields = (
            'image',
            'video',
            'create_data',

        )
        read_only_fields = ('id', 'user')

