from django.core.management.base import BaseCommand
from movie.utils.movie_crawler import MovieCrawler


class Command(BaseCommand):
    help = 'This a command crawls movie info from IMDB with the given movie filename.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--file',
            required=True,
            help='Input movie file name.'
        )
        parser.add_argument(
            '-p',
            '--path',
            help='Input movie file name.'
        )

    def handle(self, *args, **kwargs):
        crawler = MovieCrawler(file=kwargs['file'], path=kwargs['path'])
        crawler.crawl_movie()
