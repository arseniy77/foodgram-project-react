from django_filters import rest_framework as filters

from .models import Recipe


# class MultiValueCharFilter(filters.CharFilter):
#     def filter(self, qs, value):
#         # value is either a list or an 'empty' value
#         print(qs)
#         print(value)
#         values = value or []
#
#         for value in values:
#             qs = super(MultiValueCharFilter, self).filter(qs, value)
#
#         return qs

class RecipeFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author__id',)
    tags = filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='contains',
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)

