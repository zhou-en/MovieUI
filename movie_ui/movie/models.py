from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Movie(models.Model):
    title = models.CharField(max_length=256)
    release_date = models.DateField()
    runtime = models.PositiveSmallIntegerField()
    poster_path = models.CharField(max_length=256)
    overview = models.TextField()
    imdb_id = models.CharField(max_length=256, unique=True)
    imdb_rating = models.FloatField()
    imdb_movie_url = models.CharField(max_length=256)
    homepage = models.CharField(max_length=256)
    preview = models.CharField(max_length=256)
    genres = models.ManyToManyField(Genre)
    resolution = models.CharField(max_length=256, default=None)
    filename = models.CharField(max_length=256, default=None, unique=True)
