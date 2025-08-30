from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, help_text="User biography")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, help_text="User profile picture")
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
        help_text="Users following this user"
    )
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
        help_text="Users this user follows"
    )

    def __str__(self):
        return self.username

# Create your models here.
