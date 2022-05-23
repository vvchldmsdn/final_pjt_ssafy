from rest_framework import serializers
from .movie_serializers import MovieSerializer, MovieGenreSerializer
from ..models import Movie, Genre


class GenreSerializer(serializers.ModelSerializer):
    movie_genre = MovieGenreSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = '__all__'