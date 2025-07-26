from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.models import signals

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        User.Profile.objects.create(user=instance, role='Member')