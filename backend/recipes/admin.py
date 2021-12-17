from django.conf import settings
from django.contrib import admin
from .models import Tag, Recipe, RecipeTag


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