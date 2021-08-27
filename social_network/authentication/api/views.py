import datetime
from authentication.api import serializers
from authentication import renderer
from authentication import models
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


class SignUpView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (renderer.UserJSONRenderer,)
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        user = request.data.get('user', None)

        if user is None:
            raise ValidationError(
                detail='user must not be empty',
            )

        user_serializer = self.serializer_class(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return Response(user_serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (renderer.UserJSONRenderer,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        user_data = request.data.get('user', None)

        if user_data is None:
            detail = (
                'user must not be empty, please '
                'provide username and password'
            )
            raise ValidationError(
                detail=detail,
            )

        user_serializer = self.serializer_class(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = models.User.objects.get(username=user_serializer.validated_data['username'])
        user.last_login = datetime.datetime.now()
        user.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class UserAnalyticsView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserAnalyticsSerializer

    def post(self, request):
        user_data = request.data.get('user', None)
        user_analytics_serializer = self.serializer_class(data=user_data)
        user_analytics_serializer.is_valid(raise_exception=True)
        return Response(user_analytics_serializer.validated_data, status=status.HTTP_200_OK)


class UserListView(APIView):
    permission_classes = (IsAdminUser,)
    format = 'json'

    def get(self, request):
        number_of_users_str = request.query_params.get('number_of_users', 0)

        try:
            number_of_users = int(number_of_users_str)
        except TypeError:
            raise ValidationError(
                'number_of_users must be of type int',
            )

        if number_of_users < 0:
            raise ValidationError(
                'number_of_users must be non negative',
            )

        # Include only non-admin users.
        possible_users = models.User.objects.filter(is_staff=False).all()

        if number_of_users > possible_users.count():
            raise ValidationError(
                'number_of_users exceeds an existing number of users in database',
            )

        users = possible_users[:number_of_users]
        users_data = []

        for user in users:

            users_data.append({
                'username': user.username,
                "token": user.token,
            })

        return Response(data=users_data, status=status.HTTP_200_OK)
