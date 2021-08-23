from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from . import renderer
from . import models
import datetime


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

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


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
