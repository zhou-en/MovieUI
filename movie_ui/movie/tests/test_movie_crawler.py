import json

from django.test import TestCase

from movie.utils.movie_crawler import MovieCrawler


class MovieCrawlerTest(TestCase):

    def setUp(self):
        pass

    def test_parse_filename(self):
        """
        :return:
        """
        test_filename = "Logan.2017.1080p.WEB-DL.DD5.1.H264-FGT"
        movie_crawler = MovieCrawler(filename=test_filename)
        movie_title, movie_series, movie_year = movie_crawler.parse_filename(test_filename)
        expected_title = ["Logan"]
        expected_year = "2017"
        self.assertEqual(
            expected_title,
            movie_title,
            (
                f"Expected title: {expected_title},"
                f"but got: {movie_title}"
            )
        )
        self.assertEqual(
            expected_year,
            movie_year,
            (
                f"Expected year: {expected_year},"
                f"but got: {movie_year}"
            )
        )
        self.assertEqual(
            None,
            movie_series,
            (
                f"Expected series: None,"
                f"but got: {movie_series}"
            )
        )

    def test_get_resolution_from_filename(self):
        """
        :return:
        """
        test_filename = "Inner.Workings.2016.1080p.BluRay.x264-HDEX[EtHD]"
        movie_crawler = MovieCrawler(test_filename)
        resolution = movie_crawler.get_resolution_from_filename(test_filename)
        expected_resolution = '1080p'
        self.assertEqual(
            expected_resolution,
            resolution,
            (
                f"Expected resolution: {expected_resolution},"
                f"but got: {resolution}"
            )
        )

    def test_get_movie_names_from_path(self):
        """
        :return:
        """
        testing_dir = "movie_ui/movie/tests/test_movies_dir"
        mc = MovieCrawler(path=testing_dir)
        expected_filenames = [
            'Logan.2017.1080p.WEB-DL.DD5.1.H264-FGT',
            'Manchester.by.the.Sea.2016.1080p.WEB-DL.DD5.1.H264-FGT',
            'War.Machine.2017.1080p.NF.WEBRip.DD5.1.x264-SB',
            'The.Lego.Batman.Movie.2017.1080p.WEB-DL.DD5.1.H264-FGT',
            'The.Boss.Baby.2017.1080p.WEB-DL.DD5.1.H264-FGT',
            'Arrival.2016.1080p.WEB-DL.DD5.1.H264-FGT'
        ]
        self.assertSetEqual(
            set(mc.filenames),
            set(expected_filenames),
            f"Expected list of movies: {expected_filenames}, "
            f"but got {mc.filenames}"
        )

    def test_get_movie_details_by_id(self):
        """
        :return:
        """
        mc = MovieCrawler()
        testing_movie_id = 'tt2245084'
        movie_details = mc.get_movie_details_by_id(imdb_id=testing_movie_id)
        expected_details = EXPECTED_DETIALS
        self.assertDictEqual(
            movie_details,
            expected_details,
            f"Expected movie details: {expected_details}, "
            f"but got: {movie_details}"
        )


EXPECTED_DETIALS = {
    'adult': False,
    'backdrop_path': '/lv3NrraY2VRK6ImwNU3vfOPZyTi.jpg',
    'belongs_to_collection': None,
    'budget': 165000000,
    'genres': [
        {'id': 12, 'name': 'Adventure'},
        {'id': 10751, 'name': 'Family'},
        {'id': 16, 'name': 'Animation'},
        {'id': 28, 'name': 'Action'},
        {'id': 35, 'name': 'Comedy'}],
    'homepage': 'http://movies.disney.com/big-hero-6',
    'id': 177572,
    'imdb_id': 'tt2245084',
    'original_language': 'en',
    'original_title': 'Big Hero 6',
    'overview': 'The special bond that develops between plus-sized inflatable robot Baymax, and prodigy Hiro Hamada, '
                'who team up with a group of friends to form a band of high-tech heroes.',
    'popularity': 39.93,
    'poster_path': '/9gLu47Zw5ertuFTZaxXOvNfy78T.jpg',
    'production_companies': [
        {
            'id': 6125,
            'logo_path': '/tVPmo07IHhBs4HuilrcV0yujsZ9.png',
            'name': 'Walt Disney Animation Studios',
            'origin_country': 'US'
        },
        {
            'id': 2,
            'logo_path': '/4MbjW4f9bu6LvlDmyIvfyuT3boj.png',
            'name': 'Walt Disney Pictures',
            'origin_country': 'US'
        }
    ],
    'production_countries': [
        {'iso_3166_1': 'US', 'name': 'United States of America'}
    ],
    'release_date': '2014-10-24',
    'revenue': 657818612,
    'runtime': 102,
    'spoken_languages': [{'iso_639_1': 'en', 'name': 'English'}],
    'status': 'Released',
    'tagline': '',
    'title': 'Big Hero 6',
    'video': False,
    'vote_average': 7.8,
    'vote_count': 9672
}
