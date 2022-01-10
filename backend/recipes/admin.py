from django.conf import settings
from django.contrib import admin

from .models import FavouriteRecipe  # noqa
from .models import Ingredient, Recipe, RecipeIngredients, RecipeTag, Tag  # noqa
# noqa


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'name', 'text', 'cooking_time'
    )
    search_fields = ('name',)
    list_filter = ('author',)
    empty_value_display = settings.BLANK_VALUE_CONST


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'color', 'slug',
    )
    list_filter = ('name',)
    empty_value_display = settings.BLANK_VALUE_CONST


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = (
        'recipe', 'tag'
    )
    search_fields = ('tag',)
    list_filter = ('recipe',)
    empty_value_display = settings.BLANK_VALUE_CONST


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = settings.BLANK_VALUE_CONST


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'recipe', 'ingredient', 'amount',
    )
    search_fields = ('recipe',)
    list_filter = ('ingredient',)
    empty_value_display = settings.BLANK_VALUE_CONST


@admin.register(FavouriteRecipe)
class FavouriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'user', 'recipe', 'is_in_shopping_cart',
        'is_favorited', 'added_to_favourite',
    )
    search_fields = ('recipe',)
    list_filter = ('user',)
    empty_value_display = settings.BLANK_VALUE_CONST
