from movie.models import Movie, Genre
from movie.serializers import MovieSerializer, GenreSerializer
from rest_framework import generics


class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
