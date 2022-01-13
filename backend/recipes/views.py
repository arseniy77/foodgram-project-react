from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from users.permissions import AnyUserOrAnonimous  # noqa
from .file_services import import_csv
from .filters import IngredientFilter, RecipeFilter
from .models import FavouriteRecipe, Ingredient, Recipe, Tag
from .permissions import IsRecipeOwnerOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeFavouriteSerializer,
    RecipePostSerializer,
    RecipeSerializer,
    TagSerializer
)
# noqa


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsRecipeOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_in_shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        is_favorited = self.request.query_params.get('is_favorited')
        recipes_limit = self.request.query_params.get('recipes_limit')
        if is_in_shopping_cart is not None or is_favorited is not None:
            queryset = queryset.filter(author=self.request.user)
        if recipes_limit is not None:
            queryset = queryset[:int(recipes_limit)]
        return queryset

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'POST', 'PATCH'):
            return RecipePostSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (AnyUserOrAnonimous(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=('get', 'delete'),
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = self.get_object()
        if request.method == 'GET':
            if FavouriteRecipe.objects.filter(
                user=user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                FavouriteRecipe.objects.update_or_create(
                    user=user, recipe=recipe,
                    defaults={
                        'user': user,
                        'recipe': recipe,
                        'is_favorited': True
                    }
                )
                serialized_response = RecipeFavouriteSerializer(recipe)
                return Response(
                    serialized_response.data,
                    status=status.HTTP_201_CREATED
                )

        if not FavouriteRecipe.objects.filter(
                recipe=recipe,
                user=user,
        ).exists():
            return Response(
                {'errors': 'Рецепт не в списке избранного'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        fav_recipe = get_object_or_404(
            FavouriteRecipe,
            recipe=recipe, user=user
        )
        if not fav_recipe.is_favorited:
            return Response(
                {'errors': 'Рецепт не в списке избранного'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not fav_recipe.is_in_shopping_cart:
            fav_recipe.delete()
        else:
            fav_recipe.is_favorited = False
            fav_recipe.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('get', 'delete'),
            permission_classes=(permissions.IsAuthenticated),)
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = self.get_object()

        if request.method == 'GET':
            if FavouriteRecipe.objects.filter(
                    user=user,
                    recipe=recipe,
                    is_in_shopping_cart=True,
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в корзину'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            FavouriteRecipe.objects.update_or_create(
                user=user,
                recipe=recipe,
                defaults={
                    'user': user, 'recipe': recipe,
                    'is_in_shopping_cart': True
                },
            )
            return Response(
                {'status': 'Рецепт успешно добавлен в список покупок'},
                status=status.HTTP_201_CREATED
            )

        else:
            if not FavouriteRecipe.objects.filter(
                    recipe=recipe,
                    user=user,
            ).exists():
                return Response(
                    {'errors': 'Рецепт не в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            fav_recipe = get_object_or_404(
                FavouriteRecipe,
                recipe=recipe,
                user=user
            )
            if not fav_recipe.is_in_shopping_cart:
                return Response(
                    {'errors': 'Рецепт не в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not fav_recipe.is_favorited:
                fav_recipe.delete()
            else:
                fav_recipe.is_in_shopping_cart = False
                fav_recipe.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=('get'),
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request, pk=None):
        user = request.user
        recipes = Recipe.objects.filter(
            in_favourites__user=user,
            in_favourites__is_in_shopping_cart=True
        )
        ingredients = recipes.values(
            'ingredients__name',
            'ingredients__measurement_unit').order_by(
            'ingredients__name').annotate(
            ingredients_total=Sum('ingredient_amounts__amount')
        )
        shopping_list = {}
        for item in ingredients:
            title = item.get('ingredients__name')
            count = str(item.get('ingredients_total')) + ' ' + item[
                'ingredients__measurement_unit'
            ]
            shopping_list[title] = count
        data = ''
        for key, value in shopping_list.items():
            data += f'{key} - {value}\n'
        return HttpResponse(data, content_type='text/plain')


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (AnyUserOrAnonimous(),)
        return super().get_permissions()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    filterset_class = IngredientFilter


    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (AnyUserOrAnonimous(),)
        return super().get_permissions()

    @action(detail=False, methods=('get',),
            permission_classes=(permissions.IsAdminUser,))
    def import_ingredients(self, request, pk=None):
        """Импорт списка ингридиентов из файла."""
        return import_csv()
