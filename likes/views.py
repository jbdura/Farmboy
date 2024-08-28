# likes/views.py

from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from .models import Like
from .serializers import LikeSerializer, LikedPostSerializer
from post.models import Post
from comment.models import Comment


class LikeToggleView(APIView):
    """
    View to handle liking and unliking of any content (posts, comments, etc.).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, model_name, object_id):
        """
        Toggles like or unlike for a given model and object id.
        """
        # Determine the content type model dynamically
        if model_name not in ['post', 'comment']:
            return Response({"detail": "Invalid model type."}, status=status.HTTP_400_BAD_REQUEST)

        if model_name == 'post':
            ModelClass = Post
        elif model_name == 'comment':
            ModelClass = Comment

        # Check if the object exists
        try:
            content_object = ModelClass.objects.get(pk=object_id)
        except ModelClass.DoesNotExist:
            return Response({"detail": f"{model_name.capitalize()} not found."}, status=status.HTTP_404_NOT_FOUND)

        content_type = ContentType.objects.get_for_model(ModelClass)
        user = request.user

        # Check if the user has already liked the object
        existing_like = Like.objects.filter(user=user, content_type=content_type, object_id=content_object.id).first()

        if existing_like:
            # Unlike the content
            existing_like.delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Create a new like for the content
            like_data = {
                'user': user.id,
                'content_type': content_type.id,
                'object_id': content_object.id
            }
            serializer = LikeSerializer(data=like_data)
            if serializer.is_valid():
                serializer.save()
                return Response({"detail": "Like added."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikedPostsListView(generics.ListAPIView):
    """
    View to list all posts liked by the authenticated user.
    """
    serializer_class = LikedPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the content type for posts
        post_content_type = ContentType.objects.get_for_model(Post)
        # Get all likes of type 'post' by the authenticated user
        likes = Like.objects.filter(user=self.request.user, content_type=post_content_type)
        # Extract the IDs of the liked posts
        post_ids = likes.values_list('object_id', flat=True)
        # Return the posts liked by the user
        return Post.objects.filter(id__in=post_ids)

