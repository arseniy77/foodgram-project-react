from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (ADMIN, 'admin'),
    )


    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Clearance level',
    )
    confirmation_code = models.CharField(
        max_length=70, blank=True
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
