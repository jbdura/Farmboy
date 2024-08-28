# forums/views.py

from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError  # Correct import for ValidationError
from .models import Forum
from community.models import Community
from .serializers import ForumSerializer


class ForumListCreateView(generics.ListCreateAPIView):
    """
    View to list all forums in public communities or forums where the user is a member.
    Allows creation of new forums by community members.
    """
    serializer_class = ForumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return forums in public communities or where the user is a member.
        """
        user = self.request.user
        public_communities = Community.objects.filter(is_public=True)
        private_communities = Community.objects.filter(is_public=False, members=user)
        return Forum.objects.filter(community__in=(public_communities | private_communities))

    def perform_create(self, serializer):
        """
        Set the user who creates the forum as the owner.
        """
        serializer.save()

class ForumDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a forum.
    Allows updates and deletions only by the community admin or forum creator.
    """
    serializer_class = ForumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Restrict the queryset to forums in communities where the user has access.
        """
        user = self.request.user
        public_communities = Community.objects.filter(is_public=True)
        private_communities = Community.objects.filter(is_public=False, members=user)
        return Forum.objects.filter(community__in=(public_communities | private_communities))

    def perform_update(self, serializer):
        """
        Ensure only community admins or the user who created the forum can update it.
        """
        user = self.request.user
        forum = self.get_object()
        if user not in forum.community.admins.all() and forum.community.creator != user:
            raise ValidationError("You do not have permission to update this forum.")  # Corrected usage
        serializer.save()

    def perform_destroy(self, instance):
        """
        Ensure only community admins or the user who created the forum can delete it.
        """
        user = self.request.user
        if user not in instance.community.admins.all() and instance.community.creator != user:
            raise ValidationError("You do not have permission to delete this forum.")  # Corrected usage
        instance.delete()
