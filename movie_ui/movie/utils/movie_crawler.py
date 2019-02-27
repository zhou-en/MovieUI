# -*- coding: utf-8 -*-
import requests
import json
import re
from os import listdir
from os.path import isdir, join
from contextlib import closing
from bs4 import BeautifulSoup
from django.conf import settings
from requests.exceptions import RequestException

from movie.models import Movie, Genre


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers["Content-Type"].lower()
    return (
            resp.status_code == 200
            and content_type is not None
            and content_type.find("html") > -1
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

    def __init__(self, filename=None, path=None):
        self.path = path
        self.filenames = [filename] if not self.path else self.get_movie_names_from_path()
        self.not_found = []

    def get_movie_names_from_path(self):
        """
        :return: list of movie filenames
        """
        filenames = []
        try:
            for f in listdir(self.path):
                if isdir(join(self.path, f)):
                    for ff in listdir(join(self.path, f)):
                        if ff.endswith('.mkv'):
                            filenames.append(ff.replace('.mkv', ''))
                else:
                    if f.endswith('.mkv'):
                        filenames.append(f.replace('.mkv', ''))
        except OSError as msg:
            print("No movies were found in: {}".format(self.path))
        print(f"Total Movie: {len(filenames)}")
        return filenames

    def chinese_characters_in_file_name(self, filename):
        """
        :return:
        """
        print(f"Identify Chinese characters in {filename}")
        return re.findall('[\u4e00-\u9fff]+', filename)

    def remove_noise_characters_from_filename(self, filename):
        """
        :return:
        """
        for item in ['(', ')', '[', ']']:
            filename = filename.replace(item, ' ')
        return filename

    def parse_filename(self, filename):
        """
        Get movie name, year, resolution info from the given filename.
        return: title, year, resolution
        """

        filename = self.remove_noise_characters_from_filename(filename)
        filename = filename.replace(" ", ".")
        print(f"filename: {filename}")
        chinese = self.chinese_characters_in_file_name(filename)
        print(f"Chinese characters found: {chinese}")
        title_and_year = []
        split_filename = filename.split(".")

        for item in split_filename:
            if item and item not in chinese:
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
                len(title_and_year) == len(filename.split("."))
                and not title_and_year[-1].isdigit()
        ):
            print("\nERROR: Invalid movie name: No year info was found\n")

        return title, series, year

    def get_resolution_from_filename(self, filename):
        """
        :return:
        """
        if "1080p" in filename:
            return "1080p"
        if "720p" in filename:
            return "720p"
        return ""

    def search_movie(self, title, series, year):
        """
        :return bs html
        """
        search_title = f"{title} {series}" if series else f"{'+'.join(title)}"
        url = (
                f"http://www.imdb.com/search/title?title={search_title}&"
                + f"title_type=feature,video&release_date="
                + f"{year}-01-01,{year}-12-31"
        )
        # logger.info("Get movie url from {}".format(url))
        print(f"Searching for movie: {url}")
        response = simple_get(url)
        return BeautifulSoup(response, "html.parser")

    def find_match_movie_in_html_response(self, html):
        """
        :return movie url
        """
        result = html.find("h3", {"class": "lister-item-header"})
        if result:
            movie_href = result.find(href=True).get("href", None)
            return "http://www.imdb.com" + movie_href
        else:
            return None

    def get_imdb_id_from_url(self, imdb_movie_url):
        """[summary]
        """
        if imdb_movie_url:
            if imdb_movie_url.split("/")[-2].startswith("tt"):
                return imdb_movie_url.split("/")[-2]

    def get_movie_details_by_id(self, imdb_id):
        """
        https://api.themoviedb.org/3/movie/{imdb_id}?api_key=c73d7f19c33a3c43d4f4f66a80cde8d7
        original_title: string
        title: string
        release_date: string
        vote_average: number
        production_countries: list of dictionary
        original_language: string
        """
        url = f"{settings.TMDB_HOST}/3/movie/{imdb_id}?api_key={settings.TMDB_API_KEY}&format=json"
        print("Send GET request: {}".format(url))
        return requests.get(url).json()

    def get_movie_rating_by_url(self, movie_url):
        """
        Get movie title to confirm
        Get movie rating
        """
        print(f"Get movie rating from: {movie_url}")
        doc = simple_get(movie_url)
        soup = BeautifulSoup(doc, "html.parser")
        rating_div = soup.find("span", {"itemprop": "ratingValue"})
        rating_str = str(rating_div)
        return float(rating_str.replace("</span>", "").split(">")[-1])
        # logger.info("Movie Rating: {}".format(rating))
        # return rating

    @staticmethod
    def save_genres(movie_data):
        """[summary]
        """
        for genre in movie_data["genres"]:
            try:
                Genre(**{"name": genre["name"]}).save()
            except Exception as err:
                print(err)
                continue

    def save_movie(self, filename, movie_data, imdb_movie_url, imdb_id, imdb_rating):
        """
        """
        homepage = (
            imdb_movie_url
            if not movie_data.get("homepage")
            else movie_data.get("homepage")
        )
        rating = (
            imdb_rating
            if imdb_rating
            else float(movie_data.get("vote_average", None))
        )
        try:
            Movie(
                **{
                    "title": movie_data.get("title", None),
                    "release_date": movie_data.get("release_date", None),
                    "runtime": movie_data.get("runtime", None),
                    "poster_path": (
                        f"https://image.tmdb.org/t/p/w500"
                        f"{movie_data.get('poster_path', None)}"
                    ),
                    "overview": movie_data.get("overview", None),
                    "imdb_id": movie_data.get("imdb_id", None),
                    "imdb_rating": rating,
                    "imdb_movie_url": imdb_movie_url,
                    "homepage": homepage,
                    # 'trailer': self.
                    # 'geners:
                    "resolution": self.get_resolution_from_filename(filename),
                    "filename": filename,
                }
            ).save()
        except Exception as err:
            if "UNIQUE constraint failed: movie_movie.imdb_id" in str(err):
                movie = Movie.objects.get(imdb_id=imdb_id)
                if imdb_rating != movie.imdb_rating:
                    Movie.objects.filter(imdb_id=imdb_id).update(
                        **{"imdb_rating": imdb_rating}
                    )
                    print(f"{movie.title}'s rating was updated to {imdb_rating}")
                else:
                    print(f"{movie.title}'s rating remains: {movie.imdb_rating}")
            else:
                raise Exception(err)
        else:
            print(f"Saved successfully.")

    def crawl_movie(self):
        """
        """
        for filename in self.filenames:
            print(f"Starting crawling movie: {filename}")
            if not Movie.objects.filter(filename__startswith=f"{filename}"):
                title, series, year = self.parse_filename(filename)
                html = self.search_movie(title, series, year)
                imdb_movie_url = self.find_match_movie_in_html_response(html)
                if not imdb_movie_url:
                    print(f"{title} wasn't found on IMDB site.")
                    self.not_found.append(filename)
                    continue
                imdb_id = self.get_imdb_id_from_url(imdb_movie_url)
                movie_data = self.get_movie_details_by_id(imdb_id)
                imdb_rating = self.get_movie_rating_by_url(imdb_movie_url)
                print(json.dumps(movie_data, indent=4))
                self.save_movie(
                    filename=filename, movie_data=movie_data,
                    imdb_movie_url=imdb_movie_url,
                    imdb_id=imdb_id, imdb_rating=imdb_rating
                )
            else:
                movie = Movie.objects.filter(filename__startswith=f"{filename}")[0]
                print(f"This movie was saved in the database with rating of: {movie.imdb_rating}")
                # Get movie rating from IMDB site with imdb_id
                new_rating = self.get_movie_rating_by_url(movie.imdb_movie_url)
                if movie.imdb_rating != new_rating:
                    print(f'Rating was updated to [{new_rating}] on IMDB')
                    movie.imdb_rating = new_rating
                    print(f'Save the new rating.')
                    movie.save()
                else:
                    print(f'Rating is still: [{movie.imdb_rating}]')
        if self.not_found:
            print(f"Following movies were not found on IMDB: {json.dumps(self.not_found, indent=4)}")
