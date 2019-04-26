from rest_framework import generics

from .serializers import (
        UserSerializer,
    )

from rest_framework.permissions import (
        AllowAny,
        # IsAuthenticated,
        # IsAdminUser,
        # IsAuthenticatedOrReadOnly,
    )


class UserCreate(generics.CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserSerializer