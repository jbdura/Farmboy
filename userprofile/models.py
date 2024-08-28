# userprofile/models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from gallery.models import Image

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.OneToOneField(Image, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='user_profile_image')
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signal to create UserProfile
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Signal to save the UserProfile whenever the User instance is saved
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
