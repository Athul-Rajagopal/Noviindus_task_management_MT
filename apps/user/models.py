from django.contrib.auth.models import AbstractUser
from django.db import models


# custom user model
class User(AbstractUser):
    ROLE_CHOICES = (
    ('SUPERADMIN', 'Super Admin'),
    ('ADMIN', 'Admin'),
    ('USER', 'User'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    admin = models.ForeignKey(
    'self',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='users'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )


    def __str__(self):
        return f"{self.username} ({self.role})"

