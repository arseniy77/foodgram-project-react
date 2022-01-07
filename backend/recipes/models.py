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

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент', max_length=100)
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения', max_length=50)
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
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
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.text:.15}...'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
    tag = models.ForeignKey(Tag, on_delete=CASCADE)

    class Meta:
        verbose_name = 'Рецепт -> Тег'
        verbose_name_plural = 'Рецепт -> Тег'
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.recipe} -> {self.tag}'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    class Meta:
        verbose_name = 'Рецепт -> Ингредиент'
        verbose_name_plural = 'Рецепт -> Ингредиент'
        ordering = ('recipe',)
    def __str__(self):
        return f'{self.recipe} -> {self.ingredient}'


class FavouriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favourite_recipes',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='in_favourites',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='В корзине'
    )
    is_favourite = models.BooleanField(
        default=False,
        verbose_name='В избранном'
    )
    added_to_favourite = models.DateTimeField(
        auto_now_add=True,
        verbose_name='added at'
    )
    added_to_shopping_cart = models.DateTimeField(
        auto_now_add=True,
        verbose_name='added at'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite_recipe',
            )
        ]
        verbose_name = 'Favourites'
        verbose_name_plural = 'Favourites'
        ordering = ['-added_to_favourite', '-added_to_shopping_cart']

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
