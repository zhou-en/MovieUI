from django.test import TestCase

from movie.utils.movie_crawler import MovieCrawler
# Create your tests here.


class MovieCrawlerTest(TestCase):

    def setUp(self):
        pass

    def test_parse_filename(self):
        """
        :return:
        """
        test_filename = "Inner.Workings.2016.1080p.BluRay.x264-HDEX[EtHD]"
        movie_crawler = MovieCrawler(test_filename)
        movie_crawler.parse_filename()
        expected_title = ["Inner", "Workings"]
        expected_year = "2016"
        self.assertEqual(
            expected_title,
            movie_crawler.title,
            (
                f"Expected title: {expected_title},"
                f"but got: {movie_crawler.title}"
            )
        )
        self.assertEqual(
            expected_year,
            movie_crawler.year,
            (
                f"Expected year: {expected_year},"
                f"but got: {movie_crawler.year}"
            )
        )
        self.assertEqual(
            None,
            movie_crawler.series,
            (
                f"Expected series: None,"
                f"but got: {movie_crawler.series}"
            )
        )

    def test_get_resolution_from_filename(self):
        """
        :return:
        """
        test_filename = "Inner.Workings.2016.1080p.BluRay.x264-HDEX[EtHD]"
        movie_crawler = MovieCrawler(test_filename)
        resolution = movie_crawler.get_resolution_from_filename()
        expected_resolution = '1080p'
        self.assertEqual(
            expected_resolution,
            resolution,
            (
                f"Expected resolution: {expected_resolution},"
                f"but got: {resolution}"
            )
        )
