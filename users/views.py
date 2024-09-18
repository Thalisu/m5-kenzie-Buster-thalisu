from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import UserSerializer


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(e.args[0], status=400)

        try:
            USER = serializer.create(serializer.validated_data)
        except Exception as e:
            return Response(str(e), status=500)

        serializer = UserSerializer(USER)

        return Response(serializer.data, status=201)
