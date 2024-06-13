from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    coins = models.IntegerField(default=10)  # Default coins given to each user

    # Update groups and user_permissions related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Set a unique related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Set a unique related_name
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )
