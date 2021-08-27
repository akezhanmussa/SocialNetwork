from authentication import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate


class UserAnalyticsSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    date_format = "%Y-%m-%d"

    def validate(self, attrs):
        username = attrs['username']

        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            raise ValidationError(
                'user with provided username does not exist',

            )

        last_login = user.last_login.strftime(self.date_format)
        last_request = user.last_request.strftime(self.date_format)

        return {
            "last_login": last_login,
            "last_request": last_request,
        }


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

        user: models.User = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'user with this username and password does not exist'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
