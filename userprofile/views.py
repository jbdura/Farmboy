# userprofile/views.py

from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.exceptions import PermissionDenied

class UserProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ['PUT', 'PATCH'] and obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this profile.")
        return obj
