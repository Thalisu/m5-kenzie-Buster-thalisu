from rest_framework import serializers
from .models import Movie
from .models import Ratings


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(
        max_length=10, allow_blank=True, default=""
    )
    rating = serializers.ChoiceField(
        choices=Ratings.choices, default=Ratings.G
    )
    synopsis = serializers.CharField(
        max_length=1023, allow_blank=True, default=""
    )

    added_by = serializers.EmailField(source="user.email", read_only=True)

    def create(self, validated_data: dict):
        return Movie.objects.create(**validated_data)
