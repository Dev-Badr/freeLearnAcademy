from django.urls import path
from track.api.views import TrackList, TrackDetail

# from rest_framework import routers
# from track.api.views import TrackViewSet

# router = routers.DefaultRouter()
# router.register(r'api-tracks', TrackViewSet)

app_name = 'api-track'

urlpatterns = [
	path('api-tracks/', TrackList.as_view(), name='track-list'),
	path('api-tracks/<pk>/', TrackDetail.as_view(), name='track-detail'),
] 

# urlpatterns += router.urls