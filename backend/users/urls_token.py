from django.urls import include, path

from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from rest_framework.authtoken import views
from recipes.views import index
from .views import ObtainAuthToken, UserLogout

URLS = [
    path('token/login/', ObtainAuthToken.as_view(), name='login'),
    path('token/logout/', UserLogout.as_view(), name='logout'),
    path('api-token-auth/', views.obtain_auth_token),
    # path('token/logout/', get_jwt_token, name='logout'),
    # path('', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    # path('', include('djoser.urls.jwt')),

]

urlpatterns = [
    path('', include(URLS)),
]
