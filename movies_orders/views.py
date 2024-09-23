from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import MovieOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int) -> Response:
        serializer = MovieOrderSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(e.args[0], status=400)
        try:
            MOVIE_ORDER = serializer.create(
                {
                    **serializer.validated_data,
                    "user": request.user,
                    "movie_id": movie_id,
                }
            )
        except Exception as e:
            return Response(str(e), status=500)

        serializer = MovieOrderSerializer(MOVIE_ORDER)

        return Response(serializer.data, status=201)
