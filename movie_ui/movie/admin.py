from django.contrib import admin
from django.utils.html import format_html
from movie.models import *


# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


# Define the admin class
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'imdb_rating', 'release_date', 'imdb_movie_url', 'poster_path', 'homepage')
    # list_filter = ('release_date', 'imdb_rating')
    # list_display_links = ('imdb_movie_url', 'poster_path', 'homepage')

