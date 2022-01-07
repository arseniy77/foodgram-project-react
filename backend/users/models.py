from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q


class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (ADMIN, 'admin'),
    )

    email = models.EmailField(
        max_length=254,
        blank=False,
        verbose_name='E-mail',
    )

    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Имя',
    )

    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Фамилия',
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Пользовательская роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    subscription = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Подписан на'
    )

    def __str__(self):
        return f'Подписчик {self.subscriber}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'subscription'],
                name='uniq_follow'
            ),
            models.CheckConstraint(
                check=~Q(subscriber=F('subscription')),
                name='self_following'
            )
        ]
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'