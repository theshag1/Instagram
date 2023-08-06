from rest_framework import serializers
from .models import UserStoryArchived, UserPostSaved


class UserSavedStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStoryArchived
        fields = (
            'image',
            'video',
            'create_data',

        )
        read_only_fields = ('id', 'user')


class UserSavedPostSerializer(serializers.ModelSerializer):
    model = UserPostSaved
    fields = (
        'post',
        'user',
    )
    read_only_fields = ('id',)
