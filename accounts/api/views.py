from rest_framework.views import APIView
from rest_framework import generics

from .serializers import (
        UserSerializer,
        UserDetailSerializer
    )

from rest_framework.permissions import (
        AllowAny,
        IsAuthenticated,
        # IsAdminUser,
        # IsAuthenticatedOrReadOnly,
    )


class UserCreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserDetail(APIView):

    """
    Determine the current user by their token, and return their data
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
	    serializer = UserDetailSerializer(request.user)
	    return Response(serializer.data)