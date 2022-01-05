from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import Subscription, User

FIELDS = {
    'user': (
        'email',
        'id',
        'username',
        'first_name',
        'last_name',
        'is_subscribed',
    ),
    'signup': ('email', 'id', 'username', 'first_name', 'last_name', 'password',),
    'token': ('password', 'email',)
}


# class IsSubscribedField(serializers.Field):
#     def to_representation(self, value):
#         usern = self.context.user.username
#         return usern


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if self.context.get('request'):
            user = self.context['request'].user
            if user.is_anonymous:
                return False
            return Subscription.objects.filter(
                user=user, author=obj).exists()
        else:
            return False


    class Meta:
        fields = FIELDS['user']
        model = User
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }


class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(write_only=True,
                                     required=True)

    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
        ]
    )
    first_name = serializers.CharField(
        required=True,
    )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено'
            )
        return value

    class Meta:
        fields = FIELDS['signup']
        model = User


class UserJwtSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = FIELDS['token']
        model = User


#


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            if email:
                user_request = get_object_or_404(
                    User,
                    email=email,
                )
                email = user_request.username

            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    msg = ('Пользователь не активен')
                    raise serializers.ValidationError(msg)
            else:
                msg = ('Неверные логин и/или пароль')
                raise serializers.ValidationError(msg)
        else:
            msg = ('Введите логин и пароль')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('__all__')

# class TokenSerializer(AuthTokenSerializer):
#     username = serializers.CharField(required=False)
#     email = serializers.EmailField(required=True)
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#         if email and password:
#             user = authenticate(request=self.context.get('request'),
#                                 email=email, password=password)
#
#             # The authenticate call simply returns None for is_active=False
#             # users. (Assuming the default ModelBackend authentication
#             # backend.)
#             if not user:
#                 msg = ('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = ('Must111 include "username" and "password".')
#             raise serializers.ValidationError(msg, code='authorization')
#
#         attrs['user'] = user
#         return attrs