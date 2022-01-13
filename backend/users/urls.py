from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import ChangePasswordViewset, UserViewSet  # noqa
from .views import SubscriptionViewSet  # noqa

router_v1 = DefaultRouter()
router_v1.register(
    r'subscriptions',
    SubscriptionViewSet,
    basename='subscriptions'
)
router_v1.register(
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

URLS += router_v1.urls
urlpatterns = [
    path('', include(URLS)),
]
