# likes/serializers.py

from rest_framework import serializers

from post.models import Post
from .models import Like
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'content_type', 'object_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        # Ensure that the user has not already liked the content
        user = data.get('user')
        content_type = data.get('content_type')
        object_id = data.get('object_id')
        if Like.objects.filter(user=user, content_type=content_type, object_id=object_id).exists():
            raise serializers.ValidationError("User has already liked this content.")
        return data

    def create(self, validated_data):
        return super().create(validated_data)


class LikedPostSerializer(serializers.ModelSerializer):
    """
    Serializer for posts liked by a user.
    """
    total_likes = serializers.ReadOnlyField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'post_type', 'forum', 'tags', 'created_at', 'updated_at', 'total_likes', 'is_liked_by_user']

    def get_is_liked_by_user(self, obj):
        """
        Determine if the current user has liked this post.
        """
        user = self.context['request'].user
        return Like.objects.filter(user=user, content_type__model='post', object_id=obj.id).exists()