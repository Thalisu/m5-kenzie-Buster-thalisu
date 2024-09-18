from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserSerializer(serializers.Serializer):
    username_validator = UnicodeUsernameValidator()

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=127)
    username = serializers.CharField(
        max_length=150, validators=[username_validator]
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    is_employee = serializers.BooleanField(default=False)
    password = serializers.CharField(write_only=True)
