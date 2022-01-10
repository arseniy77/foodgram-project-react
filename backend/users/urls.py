from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import ChangePasswordViewset, UserViewSet  # noqa
from .views import SubscriptionViewSet  # noqa

router = DefaultRouter()
router.register(
    r'subscriptions',
    SubscriptionViewSet,
    basename='subscriptions'
)
router.register(
    r'',
    UserViewSet,
    basename=r'users'
)


URLS = [
    path(
        'set_password/',
        ChangePasswordViewset.as_view(),
        name='set_password'
    ),
]

URLS += router.urls
urlpatterns = [
    path('', include(URLS)),
]
