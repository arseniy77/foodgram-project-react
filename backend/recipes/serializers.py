from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Recipe, Tag



class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'cooking_time',)