from django.core.management.base import BaseCommand
from movie.utils.update_movie_trailer import update_movie_trailer


class Command(BaseCommand):
    help = 'This a command adds movie trailer url if it does not have one.'

    def handle(self, *args, **kwargs):
        update_movie_trailer()
