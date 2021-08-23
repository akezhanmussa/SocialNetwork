from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from . import models
import enum


class PostOperation(str, enum.Enum):
    LIKE = 'like'
    UNLIKE = 'unlike'


class PostOperationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        post_id = request.data.get('id', None)
        post_operation = request.data.get('operation', None)

        if post_id is None:
            raise ValidationError(
                'post id must not be empty',
            )

        if post_operation is None:
            raise ValidationError(
                f'post operation must not be empty or be other than '
                f'possible choices: {[e for e in PostOperation]}'
            )

        try:
            post = models.Post.objects.get(pk=int(post_id))
            if post_operation == PostOperation.LIKE:
                post.likes.add(user)
            else:
                post.likes.remove(user)
        except models.Post.DoesNotExist as e:
            raise ValidationError(
                'post with given id does not exist',
            ) from e

        return Response(status=status.HTTP_204_NO_CONTENT)
