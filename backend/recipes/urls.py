from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, TagViewSet

app_name = 'recipes'
router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename=r'^recipes')
router.register(r'tags', TagViewSet, basename=r'^tags')

urlpatterns = [
    path('', include(router.urls)),
]
