from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)

from users.permissions import AnyUserOrAnonimous
from .filters import RecipeFilter
from .models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action in ['retrieve', 'list',]:
            # Вернем обновленный перечень используемых пермишенов
            return (AnyUserOrAnonimous(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()


        # def get_queryset(self):
    #     name = get_object_or_404(Recipe, id=self.kwargs.get('name_id'))
    #     return Recipe.objects.filter(name=name)

    # def perform_create(self, serializer):
    #     name = get_object_or_404(Recipe, id=self.kwargs.get('name_id'))
    #     serializer.save(author=self.request.user, name=name)

    # def get_queryset(self):
    #     qs = self.queryset
    #     if len(self.request.query_params) > 0:
    #         for p in self.request.query_params:
    #             for f in self.filterset_fields:
    #                 if p == f:
    #                     qs = qs.filter(**{'%s__in' % f: self.request.query_params.getlist(p)})
    #     return qs

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

def index(request):
    print('index заглушка')
    return HttpResponse('У меня получилось! Пыщ-Пыщ!!')


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)

    def get_permissions(self):
        if self.action in ['retrieve', 'list',]:
            return (AnyUserOrAnonimous(),)
        return super().get_permissions()




