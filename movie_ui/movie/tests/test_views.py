import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Movie
from ..serializers import MovieSerializer


class TestViews(TestCase):
        pass
