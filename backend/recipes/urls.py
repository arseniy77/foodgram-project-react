from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'recipes'
router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename=r'^tags')
router.register(r'ingredients', IngredientViewSet, basename=r'^ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
