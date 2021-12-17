from django.urls import include, path

from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, get_jwt_token, signup
from rest_framework.authtoken import views

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

URLS = [
    path('signup/', signup, name='signup'),
    path('token/', get_jwt_token, name='token'),
    path('', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('', include('djoser.urls.jwt')),

]

URLS += router.urls

urlpatterns = [
    path('', include(URLS)),
]
