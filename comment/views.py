# comments/views.py

from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.exceptions import PermissionDenied


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the user to the currently logged-in user
        serializer.save(user=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        comment = super().get_object()
        # Check if the user is the author of the comment for updates and deletion
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and comment.user != self.request.user:
            raise PermissionDenied("You do not have permission to modify this comment.")
        return comment
