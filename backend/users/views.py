from rest_framework.views import APIView

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action

from rest_framework import parsers, renderers
from rest_framework.pagination import LimitOffsetPagination

# from foodgram.settings import DEFAULT_FROM_EMAIL
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import Subscription, User
from .permissions import AnyUserOrAnonimous
from .serializers import (UserSerializer,
                          SubscriptionSerializer,
                          UserSignupSerializer,
                          AuthCustomTokenSerializer,
                          ChangePasswordSerializer,
                          )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AnyUserOrAnonimous]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'id'
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSignupSerializer
        return UserSerializer




    @action(
        methods=['PATCH'],
        detail=True,
        permission_classes=[permissions.IsAdminUser],
    )
    def perform_update(self, serializer):
        role = serializer.validated_data.get('role')
        if role is not None:
            if role == User.ADMIN:
                serializer.save(is_staff=True, is_superuser=True)
            if role == User.MODERATOR:
                serializer.save(is_staff=True, is_superuser=False)
            if role == User.USER:
                serializer.save(is_staff=False, is_superuser=False)
        else:
            serializer.save()

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        name='me',
        permission_classes=[permissions.IsAuthenticated],
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

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        name='subscriptions',
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        subscription_list = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscription_list, many=True)
        return Response(serializer.data)




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
    permission_classes = [permissions.IsAuthenticated,]
    def post(self, request):
        request.user.auth_token.delete()
        return Response('null', status=status.HTTP_200_OK)


class ChangePasswordViewset(APIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("current_password")):
                return Response({"current_password": ['Неверный пароль.']}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SubscriptionViewSet(viewsets.ModelViewSet):
#     queryset = Subscription.objects.all()
#     serializer_class = SubscriptionSerializer
#     permission_classes = (AnyUserOrAnonimous,)


# @api_view(['POST'])
# def signup(request):
#     serializer = AuthCustomTokenSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.save()
#     user.confirmation_code = default_token_generator.make_token(user)
#     mail_subject = 'confirm code'
#     message = f'Your confirm code: {user.confirmation_code}'
#     send_mail(
#         mail_subject,
#         message,
#         DEFAULT_FROM_EMAIL,
#         [user.email],
#         fail_silently=False,
#         auth_user=user.username,
#     )
#     return Response(
#         {'email': user.email, 'username': user.username},
#         status=status.HTTP_200_OK
#     )


# @api_view(['POST'])
# def get_jwt_token(request):
#     serializer = UserJwtSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     email = serializer.validated_data.get('email')
#     password = serializer.validated_data.get('password')
#     print(password)
#     user = get_object_or_404(User, email=email)
#     print('-->', user.password, '<--')
#     if user.password == password:
#         user.is_active = True
#         user.save()
#         token = AccessToken.for_user(user)
#         return Response({'auth_token': f'{token}'}, status=status.HTTP_200_OK)
#     return Response('Token jwt error', status=status.HTTP_400_BAD_REQUEST)




# class CustomAuthToken(ObtainAuthToken):
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })


# class CustomAuthToken(ObtainAuthToken):
#
#     def post(self, request, *args, **kwargs):
#         serializer = TokenSerializer(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })


