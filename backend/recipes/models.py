from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models import F, Q

from django.contrib.auth.models import User, AbstractUser
User._meta.get_field('first_name').blank = False
User._meta.get_field('last_name').blank = False
User._meta.get_field('email').blank = False
AbstractUser.REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=100
    )
    color = models.CharField(verbose_name='Цвет', max_length=7)
    slug = models.SlugField(verbose_name='тег-слаг', unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True
    )
    text = models.TextField(verbose_name='Текст')
    tags = models.ManyToManyField(Tag, through='RecipeTag')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
    )


    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ('name',)

    def __str__(self):
        return f'{self.text:.15}...'




class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
    tag = models.ForeignKey(Tag, on_delete=CASCADE)

    def __str__(self):
        return f'{self.recipe} -> {self.tag}'
