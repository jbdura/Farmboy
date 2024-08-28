# communities/urls.py

from django.urls import path
from .views import CommunityListCreateView, CommunityDetailView, JoinCommunityView, ManageCommunityAdminView

urlpatterns = [
    path('communities/', CommunityListCreateView.as_view(), name='community-list-create'),
    path('communities/<int:pk>/', CommunityDetailView.as_view(), name='community-detail'),
    path('communities/<int:pk>/join/', JoinCommunityView.as_view(), name='join-community'),
    path('communities/<int:pk>/manage-admin/', ManageCommunityAdminView.as_view(), name='manage-community-admin'),
]
