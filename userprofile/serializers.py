# userprofile/serializers.py

from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth import get_user_model
from gallery.models import Image

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('user', 'name', 'bio', 'profile_image_url', 'location', 'created_at', 'updated_at')

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.image.url  # Assuming 'image' is the field name in the Image model
        return None
