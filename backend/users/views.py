from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token  # noqa
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import (  # noqa
    filters,  # noqa
    parsers,  # noqa
    permissions,  # noqa
    viewsets,  # noqa
    renderers,  # noqa
    status  # noqa
)  # noqa

from .models import Subscription, User
from .permissions import AnyUserOrAnonimous
from .serializers import (  # noqa
    AuthCustomTokenSerializer,  # noqa
    ChangePasswordSerializer,  # noqa
    SubscriptionChangeSerializer,  # noqa
    SubscriptionSerializer,  # noqa
    UserSignupSerializer,  # noqa
    UserSerializer  # noqa
)  # noqa
# noqa


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AnyUserOrAnonimous,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'id'
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSignupSerializer
        elif self.action == 'subscribe':
            return SubscriptionChangeSerializer
        return UserSerializer

    @action(
        methods=('PATCH',),
        detail=True,
        permission_classes=(permissions.IsAdminUser,),
    )
    def perform_update(self, serializer):
        role = serializer.validated_data.get('role')
        if role is not None:
            if role == User.ADMIN:
                serializer.save(is_staff=True, is_superuser=True)
            if role == User.USER:
                serializer.save(is_staff=False, is_superuser=False)
        else:
            serializer.save()

    @action(
        methods=('GET', 'PATCH'),
        detail=False,
        name='me',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        role = request.data.get('role')
        if role is not None and role != user.role:
            return Response(
                {'role': 'user'},
                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=('GET', 'DELETE'),
            permission_classes=(permissions.IsAuthenticated,)
            )
    def subscribe(self, request, id=None):
        subscriber = self.request.user
        subscription = self.get_object()

        if request.method == 'GET':

            if Subscription.objects.filter(
                    subscriber=subscriber,
                    subscription=subscription).exists():
                return Response(
                    'Вы уже подписаны на этого автора',
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = {
                'subscriber': subscriber.id,
                'subscription': subscription.id,
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            response_subscription = Subscription.objects.get(
                subscriber=subscriber, subscription=subscription)
            serialized_response = SubscriptionSerializer(
                response_subscription)
            return Response(
                serialized_response.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )

        if request.method == 'DELETE':
            instance = get_object_or_404(
                Subscription,
                subscriber=subscriber,
                subscription=subscription,
            )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'auth_token': token.key,
        }
        return Response(content)


class UserLogout(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response('null', status=status.HTTP_200_OK)


class ChangePasswordViewset(APIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(
                    serializer.data.get("current_password")):
                return Response(
                    {"current_password": ['Неверный пароль.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(
            subscriber=user
        ).select_related('subscription')
