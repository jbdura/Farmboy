# forums/serializers.py

from rest_framework import serializers
from .models import Forum
from community.models import Community


class ForumSerializer(serializers.ModelSerializer):
    """
    Serializer for the Forum model.
    """
    community_name = serializers.CharField(source='community.name', read_only=True)

    class Meta:
        model = Forum
        fields = ['id', 'community', 'community_name', 'title', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """
        Ensure that the forum is associated with the correct type of community.
        """
        community = data.get('community')

        if not community.is_public and self.context['request'].user not in community.members.all():
            raise serializers.ValidationError("You must be a member of a private community to create a forum.")

        return data
