from rest_framework import serializers

from .fields import Base64ImageField  # noqa
from .models import (  # noqa
    FavouriteRecipe,  # noqa
    Ingredient,  # noqa
    Recipe,  # noqa
    RecipeIngredients,  # noqa
    Tag  # noqa
)  # noqa
from .validators import CustomMinValueValidator  # noqa
from users.serializers import UserSerializer  # noqa
# noqa


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

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
        queryset=Tag.objects.all(),)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ingredients = IngredientRecipePostSerializer(
        many=True,
    )
    cooking_time = serializers.IntegerField(
        validators=(CustomMinValueValidator(1),),
    )

    def validate_ingredients(self, value):
        ingredients = []
        for ingredient in value:
            if ingredient['id'] in ingredients:
                raise serializers.ValidationError(
                    'Ингридиенты не должны повторяться!'
                )
            ingredient_amount = ingredient['amount']
            if ingredient_amount <= 0:
                raise serializers.ValidationError(
                    'Количество ингридиента должно быть числом больше нуля!'
                )
            ingredients.append(ingredient['id'])
        return value

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

    def update(self, instance, validated_data):
        tags = validated_data.get('tags')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.image = validated_data.get('image')

        instance.save()
        instance.tags.set(tags)

        instance.ingredients.clear()

        for i in range(0, len(validated_data.get('ingredients'))):
            id = validated_data.get('ingredients')[i].get('id')
            amount = validated_data.get('ingredients')[i].get('amount')
            ingredient = Ingredient.objects.get(pk=id)
            RecipeIngredients.objects.get_or_create(
                recipe=instance,
                ingredient=ingredient,
                amount=amount,
            )
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author'
        )


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
