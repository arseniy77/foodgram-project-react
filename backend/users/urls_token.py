from django.urls import include, path
from rest_framework.authtoken import views

from .views import ObtainAuthToken, UserLogout

URLS = [
    path('token/login/', ObtainAuthToken.as_view(), name='login'),
    path('token/logout/', UserLogout.as_view(), name='logout'),
    path('api-token-auth/', views.obtain_auth_token),
]

urlpatterns = [
    path('', include(URLS)),
]
