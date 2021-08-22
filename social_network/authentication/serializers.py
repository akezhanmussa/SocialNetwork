from rest_framework import serializers
from django.contrib.auth import authenticate
from . import models


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    token = serializers.CharField(
        max_length=255,
        read_only=True,
    )

    class Meta:
        model = models.User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = models.User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'username is required for login',
            )

        if password is None:
            raise serializers.ValidationError(
                'password is required for login',
            )

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'user with this username and password does not exist'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
