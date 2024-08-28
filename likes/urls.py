# likes/urls.py

from django.urls import path
from .views import LikeToggleView, LikedPostsListView

urlpatterns = [
    path('likes/<str:model_name>/<int:object_id>/', LikeToggleView.as_view(), name='like-toggle'),
    path('liked-posts/', LikedPostsListView.as_view(), name='liked-posts'),

]
