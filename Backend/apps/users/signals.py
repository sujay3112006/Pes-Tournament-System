"""Users App Signals"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.users.models import UserProfile, UserStatistics
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when a new user is created."""
    if created:
        try:
            # Check if profile already exists
            UserProfile.objects.get(user_id=str(instance.id))
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(
                user_id=str(instance.id),
                username=instance.username,
                email=instance.email,
                full_name=instance.get_full_name(),
            )


@receiver(post_save, sender=User)
def create_user_statistics(sender, instance, created, **kwargs):
    """Create user statistics when a new user is created."""
    if created:
        try:
            # Check if statistics already exist
            UserStatistics.objects.get(user_id=str(instance.id))
        except UserStatistics.DoesNotExist:
            UserStatistics.objects.create(
                user_id=str(instance.id),
            )
