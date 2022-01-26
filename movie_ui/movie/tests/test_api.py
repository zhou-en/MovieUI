import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Movie

from rest_framework.test import RequestsClient

#
# response = client.get('http://testserver/users/')
# assert response.status_code == 200


class TestViews(TestCase):
    """
    https://realpython.com/test-driven-development-of-a-django-restful-api/#get-single
    """
    def setUp(self):
        self.client = RequestsClient()
        self.test_111 = Movie.objects.create(
            title='Test 111', imdb_id='tt1111111', filename='test.111.1080p.9999.mkv', imdb_rating=1.1, release_date='1111-11-11')
        self.test_222 = Movie.objects.create(
            title='Test 222', imdb_id='tt2222222', filename='test.222.1080p.9999.mkv', imdb_rating=2.2, release_date='2222-22-22')

    def tearDown(self):
        Movie.objects.get(title=self.test_111.title).delete()
        Movie.objects.get(title=self.test_222.title).delete()

    def test_get_movie_by_title(self):
        response = self.client.get('http://testserver/movie?title=111')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)[0]
        self.assertEqual(response_data['title'], self.test_111.title)

    def test_order_by_rating(self):
        response = self.client.get('http://testserver/movie?title=Test&order_by=imdb_rating&direction=asc')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data[0]['imdb_rating'], 2.2)
