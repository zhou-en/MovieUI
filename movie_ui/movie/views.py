from movie.models import Movie, Genre
from movie.serializers import MovieSerializer, GenreSerializer
from rest_framework import generics


class MovieList(generics.ListCreateAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        """
        :return:
        """
        queryset = Movie.objects.all()
        release_year = self.request.query_params.get('year', None)
        title_contains = self.request.query_params.get('title', None)
        order_by_field = self.request.query_params.get('order_by', 'release_date')
        direction = self.request.query_params.get('direction', 'desc')

        if release_year:
            queryset = queryset.filter(release_date__startswith=release_year)
        if title_contains:
            queryset = queryset.filter(title__contains=title_contains)

        order_by_sign = '' if direction == 'desc' else '-'
        return queryset.order_by(order_by_sign + order_by_field)


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
