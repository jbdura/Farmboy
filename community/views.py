# communities/views.py

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Community, CommunityMember, CommunityAdmin
from .serializers import CommunitySerializer, CommunityMemberSerializer
from rest_framework.exceptions import PermissionDenied

User = get_user_model()


class CommunityListCreateView(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter communities based on privacy settings and user membership."""
        user = self.request.user
        if user.is_authenticated:
            return Community.objects.all()
        return Community.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save()


class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter communities based on privacy settings and user membership."""
        user = self.request.user
        if user.is_authenticated:
            return Community.objects.all()
        return Community.objects.filter(is_public=True)

    def perform_update(self, serializer):
        """Allow updates only by community admins."""
        community = self.get_object()
        user = self.request.user
        if not CommunityAdmin.objects.filter(community=community, user=user).exists():
            raise PermissionDenied("Only community admins can update the community.")
        serializer.save()


class JoinCommunityView(APIView):
    """Allow a user to join a community."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, format=None):
        community = Community.objects.get(pk=pk)
        user = request.user

        if community.is_public:
            CommunityMember.objects.get_or_create(community=community, user=user)
            return Response({"message": "You have successfully joined the community."})
        else:
            return Response({"message": "This is a private community. You need an invite to join."}, status=403)


class ManageCommunityAdminView(APIView):
    """Allow a community admin to add or remove other community admins."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, format=None):
        community = Community.objects.get(pk=pk)
        user = request.user

        # Check if the user making the request is an admin
        if not CommunityAdmin.objects.filter(community=community, user=user).exists():
            raise PermissionDenied("Only community admins can manage other admins.")

        # Add or remove an admin
        target_user_id = request.data.get("user_id")
        action = request.data.get("action")

        try:
            target_user = User.objects.get(pk=target_user_id)
            if action == "add":
                CommunityAdmin.objects.get_or_create(community=community, user=target_user)
                CommunityMember.objects.get_or_create(community=community, user=target_user)
                return Response({"message": f"{target_user.username} has been added as an admin."})
            elif action == "remove":
                CommunityAdmin.objects.filter(community=community, user=target_user).delete()
                return Response({"message": f"{target_user.username} has been removed as an admin."})
            else:
                return Response({"message": "Invalid action. Use 'add' or 'remove'."}, status=400)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=404)
