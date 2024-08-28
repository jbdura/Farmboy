# posts/serializers.py

from rest_framework import serializers
from .models import Post, Tag
from django.core.exceptions import ValidationError


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Display author's username
    total_likes = serializers.ReadOnlyField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'post_type', 'forum', 'tags', 'created_at', 'updated_at', 'total_likes']

    def validate(self, data):
        """
        Custom validation for forum posts to ensure they have at least one tag.
        """
        if data['post_type'] == 'forum' and not data.get('tags'):
            raise ValidationError("Forum posts must have at least one tag.")
        return data

    def create(self, validated_data):
        """
        Override the create method to ensure the author is the logged-in user.
        """
        request = self.context.get('request')
        user = request.user
        validated_data['author'] = user
        return super().create(validated_data)
