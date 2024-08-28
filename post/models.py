# # # posts/models.py
import shortuuid
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from likes.models import Like
from AgriSocial import settings
from django.core.exceptions import ValidationError

User = get_user_model()

# from gallery.models import Image


class Tag(models.Model):
    """
    These are tags models. Tags that are referred to posts
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    These are posts models.
    """
    POST_TYPE_CHOICES = [  # You can add more choices if need be
        ('profile', 'Profile Post'),
        ('forum', 'Forum Post'),
    ]

    id = models.CharField(primary_key=True, max_length=22, default=shortuuid.uuid, editable=False)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    # photos = models.ManyToManyField(Image, blank=True, related_name='posts')
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='profile')
    forum = models.ForeignKey('forum.Forum', null=True, blank=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return f"{self.author.username}'s Post"

    @property
    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        if self.post_type == 'forum' and not self.tags.exists():
            raise ValidationError("Forum posts must have at least one tag.")
        super().save(*args, **kwargs)

