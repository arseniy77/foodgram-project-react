from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)

from .models import Tag, Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination

    # def get_queryset(self):
    #     name = get_object_or_404(Recipe, id=self.kwargs.get('name_id'))
    #     return Recipe.objects.filter(name=name)

    # def perform_create(self, serializer):
    #     name = get_object_or_404(Recipe, id=self.kwargs.get('name_id'))
    #     serializer.save(author=self.request.user, name=name)


def index(request):
    return HttpResponse('У меня получилось! Пыщ-Пыщ!!')