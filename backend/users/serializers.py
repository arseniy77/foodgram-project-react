from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User

FIELDS = {
    'user': (
        'first_name',
        'last_name',
        'username',
        'email',
        'role',
    ),
    'signup': ('email', 'username'),
    'token': ('username', 'confirmation_code')
}


class UserSerializer(serializers.ModelSerializer):

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
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = FIELDS['signup']
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username звпрещено'
            )
        return value


class UserJwtSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = FIELDS['token']
        model = User
