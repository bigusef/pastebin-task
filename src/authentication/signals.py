from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance, created, **kwargs):
    """
    this function it's sgnail fire when create new user account to create new user profile and user token
    """
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
