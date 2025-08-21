from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser with additional fields.
    """
    bio = models.TextField(blank=True, help_text="User biography")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, help_text="User profile picture")
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
        help_text="Users following this user"
    )

    def __str__(self):
        return self.username
# Create your models here.
