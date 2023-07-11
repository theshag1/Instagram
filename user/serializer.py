from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from follow.models import Follow
from user.models import User
from django.utils.translation import gettext_lazy as _


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


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'Bio',
            'password'

        )
        read_only_fields = ('id',)

        def validate(self, attrs):
            password = attrs.get('password')
            if not password:
                raise ValidationError(_('Password did not match'))
            return super().validate(attrs)

        def create(self, validated_data):
            password = validated_data.pop('password', )
            user = User(**validated_data)
            user.set_password(make_password())
            user.save()
            return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    ask_validate = serializers.CharField(max_length=3)


class UserUpdateView(serializers.ModelSerializer):
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
        )
        read_only_fields = ('id',)


class Follows(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = (
            'follow',
            'followed_user'
        )
        read_only_fields = ('id',)


class Password_Update(serializers.Serializer):
    username = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()
