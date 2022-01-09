from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .fields import Base64ImageField
from .models import Ingredient, Recipe, RecipeIngredients, Tag
from .models import FavouriteRecipe
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(
        many=True, read_only=True, source='ingredient_amounts')
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def get_is_favorited(self, obj):
        if self.context.get('request'):
            user = self.context['request'].user
            if user.is_anonymous:
                return False
            return FavouriteRecipe.objects.filter(
                user=user,
                recipe=obj,
                is_favorited=True,
            ).exists()
        else:
            return False

    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request'):
            user = self.context['request'].user
            if user.is_anonymous:
                return False
            return FavouriteRecipe.objects.filter(
                user=user,
                recipe=obj,
                is_in_shopping_cart=True,
        ).exists()
        else:
            return False

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class RecipePostSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # # ingredients = serializers.SlugRelatedField(
    # #     slug_field='ingredient',
    # #     queryset=Ingredient.objects.all())
    # def get_author(self):
    #     return self.context['request'].user

    class Meta:
        model = Recipe
        fields = ('tags', 'image', 'name', 'text', 'cooking_time', 'author')


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    measurement_unit = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeFavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
