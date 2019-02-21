from django.db import models
from datetime import datetime


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Movie(models.Model):
    title = models.CharField(max_length=256, blank=True, default='')
    release_date = models.CharField(max_length=256, blank=True, default='')
    runtime = models.PositiveSmallIntegerField(blank=True, default=0)
    poster_path = models.CharField(max_length=256, blank=True, default='')
    overview = models.TextField(blank=True, default='')
    imdb_id = models.CharField(max_length=256, unique=True)
    imdb_rating = models.FloatField(blank=True, default=0.0)
    imdb_movie_url = models.CharField(max_length=256, blank=True, default='')
    homepage = models.CharField(max_length=256, blank=True, default='')
    # trailer = models.CharField(max_length=256, blank=True, default='')
    # genres = models.ManyToManyField(Genre, blank=True, default='')
    resolution = models.CharField(max_length=256, blank=True, default='')
    filename = models.CharField(max_length=256, unique=True)
    date_added = models.DateField(blank=True, default=datetime.now)
