from django.urls import path
from . import views

urlpatterns = [
    path('movie/', views.MovieListCreate.as_view()),
]