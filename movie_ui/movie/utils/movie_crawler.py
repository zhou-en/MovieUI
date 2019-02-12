# -*- coding: utf-8 -*-
import requests
import json
from contextlib import closing
from bs4 import BeautifulSoup
from django.conf import settings
from requests.exceptions import RequestException

from movie.models import Movie, Genre


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (
        resp.status_code == 200
        and content_type is not None
        and content_type.find('html') > -1
    )


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(requests.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        # log_error('Error during requests to {0}: {1}'.format(url, str(e)))
        return None


class MovieCrawler(object):
    """
    This class is used to:
        0. parse a filename and get the movie title, year, and resolution
        1. crawl movie rating and id from IMDB site
        2. send API call to The Movie Database with the id
        3. save the API response to database
    """

    def __init__(self, filename):
        self.filename = filename
        self.title = None
        self.year = None
        self.series = None
        self.html = None
        self.imdb_movie_url = None
        self.imdb_id = None
        self.imdb_rating = None

    def parse_filename(self):
        """
        Get movie name, year, resolution info from the given filename.
        return: title, year, resolution
        """
        title_and_year = []
        for item in self.filename.split("."):
            item = item.replace("(", "").replace(")", "")
            if item.isdigit() and len(item) == 4:
                title_and_year.append(item)
                break
            else:
                title_and_year.append(item)

        year = f"{title_and_year[-1]}"
        series = title_and_year[-2]
        if series.isdigit():
            title = title_and_year[:-2]
        else:
            title = title_and_year[:-1]
            series = None

        # In the case there is no year info in the name
        if (
            len(title_and_year) == len(self.filename.split(".")) and
            not title_and_year[-1].isdigit()
        ):
            print("\nERROR: Invalid movie name: No year info was found\n")

        self.year = year
        self.title = title
        self.series = series
        # return " ".join(title), series, year

    def get_resolution_from_filename(self):
        """
        :return:
        """
        if '1080p' in self.filename:
            return '1080p'
        if '720p' in self.filename:
            return '720p'
        return ''

    def search_movie(self):
        """[summary]
        """
        search_title = \
            f"{self.title} {self.series}" if self.series else f"{self.title}"
        url = (
            f"http://www.imdb.com/search/title?title={search_title}&" +
            f"title_type=feature&release_date=" +
            f"{self.year}-01-01,{self.year}-12-31"
        )
        # logger.info("Get movie url from {}".format(url))
        # logger.info("Searching for movie: {}".format(url))
        response = simple_get(url)
        self.html = BeautifulSoup(response, "html.parser")

    def find_match_movie_in_html_response(self):
        """[summary]
        """
        result = self.html.find("h3", {"class": "lister-item-header"})
        if result:
            movie_href = result.find(href=True).get("href", None)
            self.imdb_movie_url = "http://www.imdb.com" + movie_href
    #
    # def get_trailer_address_from_html_reponse(self):
    #     """
    #     :return:
    #     """

    def get_imdb_id_from_url(self):
        """[summary]
        """
        if self.imdb_movie_url:
            if self.imdb_movie_url.split("/")[-2].startswith("tt"):
                self.imdb_id = self.imdb_movie_url.split("/")[-2]

    def get_movie_details_by_id(self):
        """
        https://api.themoviedb.org/3/movie/{imdb_id}?api_key=c73d7f19c33a3c43d4f4f66a80cde8d7
        original_title: string
        title: string
        release_date: string
        vote_average: number
        production_countries: list of dictionary
        original_language: string
        """
        url = \
            f"{settings.TMDB_HOST}/3/movie/{self.imdb_id}?api_key={settings.TMDB_API_KEY}&format=json"
        print("Send GET request: {}".format(url))
        self.movie_data = requests.get(url).json()
        # TODO: 3. Get poster: https://image.tmdb.org/t/p/w500/{poster_path}

    def get_movie_rating_by_url(self):
        """
        Get movie title to confirm
        Get movie rating
        """
        # logger.info("Get movie rating from: {}".format(url))
        doc = simple_get(self.imdb_movie_url)
        soup = BeautifulSoup(doc, "html.parser")
        rating_div = soup.find('span', {"itemprop": 'ratingValue'})
        rating_str = str(rating_div)
        # if verify:
        #     verify_searched_results(url, soup)
        # Get rating
        self.imdb_rating = rating_str.replace('</span>', "").split(">")[-1]
        # logger.info("Movie Rating: {}".format(rating))
        # return rating

    def save_genres(self):
        """[summary]
        """
        for genre in self.movie_data['genres']:
            try:
                Genre(**{'name': genre['name']}).save()
            except Exception as err:
                print(err)
                continue

    # def get_genres_from_list_data(self, geners):
    #     """
    #     :param geners:
    #     :return:
    #     """
    #     for gener in geners:
    #         if not Genre.objects.filter(name=gener['name']):
    #             Genre(**{
    #                 'name': gener['name']
    #             }).save()
    #         return []

    def save_movie(self):
        # """[summary]
        # """
        homepage = self.imdb_movie_url if self.movie_data.get('homepage') == 'null'
        try:
            Movie(
                **{
                    'title': self.movie_data.get('title', None),
                    'release_date': self.movie_data.get('release_date', None),
                    'runtime': self.movie_data.get('runtime', None),
                    'poster_path': (
                        f"https://image.tmdb.org/t/p/w500"
                        f"{self.movie_data.get('poster_path', None)}"
                    ),
                    'overview': self.movie_data.get('overview', None),
                    'imdb_id': self.movie_data.get('imdb_id', None),
                    'imdb_rating': self.movie_data.get('vote_average', None),
                    'imdb_movie_url': self.imdb_movie_url,
                    'homepage': homepage,
                    # 'trailer': self.
                    # 'geners:
                    'resolution': self.get_resolution_from_filename(),
                    'filename': self.filename

                }
            ).save()
        except Exception as err:
            print(f'Save failed: {err}')
        else:
            print(f'Saved successfully.')

    def crawl_movie(self):
        """[summary]
        """
        if not Movie.objects.filter(filename__startswith=f'{self.filename}'):
            print(f"Starting crawling movie: {self.filename}")
            self.parse_filename()
            self.search_movie()
            self.find_match_movie_in_html_response()
            self.get_imdb_id_from_url()
            self.get_movie_details_by_id()
            self.get_movie_rating_by_url()
            print(json.dumps(self.movie_data, indent=4))
            self.save_movie()
            print(self.imdb_rating)
        else:
            print(f'This movie is saved in the database.')
