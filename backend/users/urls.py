from django.urls import include, path

from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, ChangePasswordViewset
from rest_framework.authtoken import views

router = DefaultRouter()
router.register(r'', UserViewSet, basename=r'users')

URLS = [
    path('set_password/', ChangePasswordViewset.as_view())
    # path('signup/', signup, name='signup'),
    # path('token/', get_jwt_token, name='token'),
    # path('', include('djoser.urls')),
]

URLS += router.urls
urlpatterns = [
    path('', include(URLS)),
]
