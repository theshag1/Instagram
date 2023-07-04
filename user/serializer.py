from rest_framework import serializers

from follow.models import Follow
from user.models import User


class UserSerilizer(serializers.ModelSerializer):
    # followers = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'Website',
            'Bio',
            'Phone_number',
            'email',
            'Gander',
            'follower',
            'followed',
            'post'
        )

        read_only_fields = ('id',)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
