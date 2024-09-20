from django.urls import path
from movies.views import MovieView

urlpatterns = [
    path("movies/", MovieView.as_view()),
]
