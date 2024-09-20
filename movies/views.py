from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import MovieSerializer
from .models import Movie
from .permissions import IsAdminOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication


class MovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(e.args[0], status=400)
        try:
            MOVIE = serializer.create(
                {**serializer.validated_data, "user": request.user}
            )
        except Exception as e:
            return Response(str(e), status=500)

        serializer = MovieSerializer(MOVIE)

        return Response(serializer.data, status=201)

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()
        return Response([MovieSerializer(movie).data for movie in movies])


class OneMovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request, movie_id) -> Response:
        try:
            MOVIE = Movie.objects.get(pk=movie_id)
        except (Movie.DoesNotExist, ValueError):
            return Response({"message": "Movie not found"}, status=404)

        return Response(MovieSerializer(MOVIE).data)

    def delete(self, request: Request, movie_id) -> Response:
        try:
            Movie.objects.get(pk=movie_id).delete()
        except (Movie.DoesNotExist, ValueError):
            return Response({"message": "Movie not found"}, status=404)

        return Response(status=204)
