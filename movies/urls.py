from django.urls import path
from movies.views import MovieView, OneMovieView

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/", OneMovieView.as_view()),
]
