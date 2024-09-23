from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import User
from .permissions import IsEmployeeOrSameUser


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


class OneUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployeeOrSameUser]

    def get(self, request: Request, user_id: int) -> Response:
        try:
            USER = User.objects.get(pk=user_id)
            self.check_object_permissions(request, USER)
        except (User.DoesNotExist, ValueError):
            return Response({"message": "User not found"}, status=404)

        return Response(UserSerializer(USER).data)

    def patch(self, request: Request, user_id: int) -> Response:
        try:
            USER = User.objects.get(pk=user_id)
            self.check_object_permissions(request, USER)
        except (User.DoesNotExist, ValueError):
            return Response({"message": "User not found"}, status=404)

        serializer = UserSerializer(USER, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(e.args[0], status=400)

        try:
            USER = serializer.save()
        except Exception as e:
            return Response(str(e), status=500)

        serializer = UserSerializer(USER)

        return Response(serializer.data, status=200)
