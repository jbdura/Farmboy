# posts/views.py

from rest_framework import generics, permissions
from .models import Post, Tag
from .serializers import PostSerializer, TagSerializer
from rest_framework.exceptions import PermissionDenied

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the author to the currently logged-in user
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        post = super().get_object()
        # Check if the user is the author of the post for updates and deletion
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and post.author != self.request.user:
            raise PermissionDenied("You do not have permission to modify this post.")
        return post


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
