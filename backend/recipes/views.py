from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)

from .filters import RecipeFilter
from .models import Tag, Recipe
from .serializers import RecipeSerializer, TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

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
    return HttpResponse('У меня получилось! Пыщ-Пыщ!!')