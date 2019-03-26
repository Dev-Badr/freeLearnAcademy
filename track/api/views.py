from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView

from track.models import Track
from track.api.serializers import TrackSerializer

# manualy
# from rest_framework.views import APIView
# from rest_framework import status

# class TrackList(APIView):
# 	def get(self, request, format=None):
# 		tracks = Track.objects.all()
# 		serializer = TrackSerializer(tracks, many=True)
# 		return Response(serializer.data)

# 	def post(self, request, format=None):
# 		serializer = TrackSerializer(data=request.data)
# 		serializer.is_valid(raise_exception=True)
# 		serializer.save()
# 		return Response(serializer.data, status=status.HTTP_201_CREATED)

class TrackList(ListAPIView):
	queryset = Track.objects.all()
	serializer_class = TrackSerializer

class TrackDetail(RetrieveAPIView):
	queryset = Track.objects.all()
	serializer_class = TrackSerializer

# The ModelViewSet class inherits from GenericAPIView and includes implementations for various actions,
# by mixing in the behavior of the various mixin classes.

# The actions provided by the ModelViewSet class are .list(), .retrieve(), .create(), .update(),
# .partial_update(), and .destroy().

# Example

# Because ModelViewSet extends GenericAPIView, you'll normally need to provide at least
# the queryset and serializer_class attributes. For example:

# from rest_framework import viewsets

# class TrackViewSet(viewsets.ModelViewSet):
#     """
#     A simple ViewSet for viewing and editing accounts.
#     """
#     queryset = Track.objects.all()
#     serializer_class = TrackSerializer