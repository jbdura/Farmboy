# comments/serializers.py

from rest_framework import serializers
from .models import Comment
from likes.models import Like

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display user's username
    total_likes = serializers.ReadOnlyField()
    replies = serializers.SerializerMethodField()  # For nested replies

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'user', 'content', 'parent_comment',
            'created_at', 'updated_at', 'total_likes', 'replies'
        ]

    def get_replies(self, obj):
        # Fetch replies related to the current comment
        replies = Comment.objects.filter(parent_comment=obj)
        return CommentSerializer(replies, many=True).data

    def create(self, validated_data):
        # Override create method to ensure the user is set to the logged-in user
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure only content can be updated
        if 'user' in validated_data:
            validated_data.pop('user')
        return super().update(instance, validated_data)
