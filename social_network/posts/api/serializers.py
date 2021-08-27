from posts import models
from posts import constants
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        post_id = attrs['id']

        try:
            post = models.Post.objects.get(id=post_id)
            return {
                'description': post.description,
                'likes': post.likes.count(),
            }
        except models.Post.DoesNotExist:
            raise ValidationError(
                f'post with id {post_id} does not exist',
            )


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['id', 'user', 'description']
        read_only_fields = ['id']


class PostOperationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    operation = serializers.ChoiceField(
        choices=[
            constants.PostOperation.LIKE.value,
            constants.PostOperation.UNLIKE.value,
        ]
    )

    def validate(self, attrs):
        try:
            post = models.Post.objects.get(pk=attrs['id'])
        except models.Post.DoesNotExist:
            raise ValidationError(
                f'post with {attrs["id"]} does not exist',
            )
        attrs['post'] = post
        return attrs
