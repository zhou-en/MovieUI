from rest_framework import serializers
from movie.models import Movie, Genre


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # fields = '__all__'
        fields = ["title", "release_date", "imdb_id", "imdb_rating", "imdb_movie_url", "trailer"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
