from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def CreateProfile(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)


