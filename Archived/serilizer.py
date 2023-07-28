from rest_framework import serializers

from Archived.models import UserStoryArchived


class ArchivedStorySerizlier(serializers.Serializer):
    class Meta:
        model = UserStoryArchived
        fields = (

        )
