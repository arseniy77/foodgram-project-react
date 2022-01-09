from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.response import Response

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


class IngredientPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(required=False)

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipePostSerializer(
        many=True, read_only=True,)
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

# class RecipePostAnswerSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Recipe
#         fields = ('__all__')

class RecipePostSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ingredients = IngredientRecipePostSerializer(many=True,)
    # ingredients = serializers.SlugRelatedField(
    #     many=True,
    #     slug_field='amount',
    #     queryset=RecipeIngredients.objects.all()
    # )

    def create(self, validated_data):

        tags = validated_data.get('tags')
        recipe = Recipe(
            author=self.context.get('request').user,
            name=validated_data.get('name'),
            text=validated_data.get('text'),
            cooking_time=validated_data.get('cooking_time'),
            image=validated_data.get('image'),
        )
        recipe.save()
        recipe.tags.set(tags)

        for i in range(0, len(validated_data.get('ingredients'))):
            id = validated_data.get('ingredients')[i].get('id')
            amount = validated_data.get('ingredients')[i].get('amount')
            ingredient = Ingredient.objects.get(pk=id)
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount,
            )
        return recipe


        # # amount = self.initial_data['ingredients'][0]['amount']
        # tags = validated_data.pop('tags')
        # # Уберем список достижений из словаря validated_data и сохраним его
        # ingredients = validated_data.pop('ingredients')
        # a = validated_data
        #
        # # Создадим нового котика пока без достижений, данных нам достаточно
        # recipe = Recipe.objects.create(**validated_data)
        # recipe.tags.set(tags)
        #
        # # Для каждого достижения из списка достижений
        # for ingredient in ingredients:
        #     b = ingredient
        #     print(b)
        #     # Создадим новую запись или получим существующий экземпляр из БД
        #     current_ingredient, status = Ingredient.objects.get_or_create(
        #         **ingredient,)
        #     # Поместим ссылку на каждое достижение во вспомогательную таблицу
        #     # Не забыв указать к какому котику оно относится
        #     RecipeIngredients.objects.create(
        #         ingredient=current_ingredient, recipe=recipe, amount=50)
        # return recipe

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text', 'cooking_time', 'author')


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
