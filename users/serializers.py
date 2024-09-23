from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from users.models import User


class UserSerializer(serializers.Serializer):
    username_validator = UnicodeUsernameValidator()

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="email already registered.",
            )
        ],
    )
    username = serializers.CharField(
        max_length=150,
        validators=[
            username_validator,
            UniqueValidator(
                queryset=User.objects.all(), message="username already taken."
            ),
        ],
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(required=False, default=None)
    is_employee = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)

    def update(self, instance: User, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    def create(self, validated_data: dict):
        return User.objects.create_user(**validated_data)
