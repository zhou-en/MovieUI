from movie.models import Movie
from movie.utils.movie_crawler import MovieCrawler


def update_movie_trailer():
    """

    :return:
    """
    for movie in Movie.objects.all():
        if not movie.trailer:
            movie_url = movie.imdb_movie_url
            movie_id = movie.imdb_id
            trailer_url = MovieCrawler.get_movie_trailer_by_url(movie_url, movie_id)
            if trailer_url:
                movie.trailer = trailer_url
                movie.save()
