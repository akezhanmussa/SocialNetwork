import datetime
import authentication.models
from . import serializers
from . import constants
from . import models
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status


class PostView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PostSerializer

    def get(self, request):
        post_data = request.data.get('post', None)
        post_serializer = self.serializer_class(data=post_data)
        post_serializer.is_valid(raise_exception=True)
        return Response(post_serializer.validated_data, status=status.HTTP_200_OK)


class PostCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PostCreateSerializer

    def post(self, request):
        post_create_data = request.data.get('post', None)
        post_create_data['user'] = request.user.id
        post_create_serializer = self.serializer_class(data=post_create_data)
        post_create_serializer.is_valid(raise_exception=True)
        post_create_serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostOperationView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PostOperationSerializer

    def post(self, request):
        user: authentication.models.User = request.user
        post_operation_serializer = self.serializer_class(data=request.data)
        post_operation_serializer.is_valid(raise_exception=True)
        post = post_operation_serializer.validated_data['post']
        now = datetime.datetime.now()

        if post_operation_serializer.validated_data['operation'] == constants.PostOperation.LIKE:
            post.likes.add(user, through_defaults={'date': now})
        else:
            post.likes.remove(user)

        # Save time when the current user made the last request to the service.
        user.last_request = now
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostAnalyticsView(APIView):
    permission_classes = (IsAuthenticated,)
    date_format = "%Y-%m-%d"

    def get(self, request):
        date_from_str = request.query_params.get('date_from', None)
        date_to_str = request.query_params.get('date_to', None)

        if date_from_str is None or date_to_str is None:
            raise ValidationError(
                'provide query parameters'
            )

        try:
            date_from = datetime.datetime.strptime(date_from_str, self.date_format)
            date_to = datetime.datetime.strptime(date_to_str, self.date_format)
            likes_num = models.PostLike.objects.filter(date__gte=date_from).filter(date__lte=date_to).count()
            return Response(
                {
                    'likes_num': likes_num,
                },
                status=status.HTTP_200_OK,
            )
        except (ValueError, TypeError):
            raise ValidationError(
                f'provided query parametrs are invalid,'
                f'make sure that both "date_from" and '
                f'"date_to" follow format: {self.date_format}',
            )
