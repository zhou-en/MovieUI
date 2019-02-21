from django.urls import path
from . import views

urlpatterns = [
    path('api/movie/', views.MovieListCreate.as_view()),
]