# communities/serializers.py

from rest_framework import serializers
from .models import Community, CommunityAdmin, CommunityMember
from django.contrib.auth import get_user_model

User = get_user_model()

class CommunityMemberSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    joined_at = serializers.ReadOnlyField()

    class Meta:
        model = CommunityMember
        fields = ('user', 'joined_at')


class CommunityAdminSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    added_at = serializers.ReadOnlyField()

    class Meta:
        model = CommunityAdmin
        fields = ('user', 'added_at')


class CommunitySerializer(serializers.ModelSerializer):
    members = CommunityMemberSerializer(many=True, read_only=True)
    admins = CommunityAdminSerializer(many=True, read_only=True)
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ('id', 'name', 'description', 'is_public', 'created_at', 'updated_at', 'members', 'admins', 'is_admin')
        read_only_fields = ('created_at', 'updated_at')

    def get_is_admin(self, obj):
        """Check if the request user is an admin of the community"""
        request = self.context.get('request')
        if request and request.user:
            return CommunityAdmin.objects.filter(community=obj, user=request.user).exists()
        return False

    def create(self, validated_data):
        """Override the create method to automatically make the creator an admin"""
        user = self.context['request'].user
        community = Community.objects.create(**validated_data)
        CommunityAdmin.objects.create(community=community, user=user)  # Make the creator an admin
        CommunityMember.objects.create(community=community, user=user)  # Also make the creator a member
        return community

