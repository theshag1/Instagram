from rest_framework import serializers
from .models import UserStoryArchived, SavedPost


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
    model = SavedPost
    fields = (
          'user',
          'post',
    )
    read_only_fields = ('id',)
