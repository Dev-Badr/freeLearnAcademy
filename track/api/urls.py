from django.urls import path

from track.api.views import (
	TrackList, TrackDetail,
	CourseList, CourseDetail,
	UnitList, UnitDetail,
	LectureList, LectureDetail,
	CourseMemberList, CourseMemberDetail,
	CategoryList, CategoryDetail,
	ArticleList, ArticleDetail,
	PracticeList, PracticeDetail
	)

# from rest_framework import routers
# from track.api.views import TrackViewSet

# router = routers.DefaultRouter()
# router.register(r'api-tracks', TrackViewSet)

app_name = 'api-track'

urlpatterns = [
	path('tracks/', TrackList.as_view()),
	path('tracks/<int:pk>/', TrackDetail.as_view()),

	path('courses/', CourseList.as_view()),
	path('courses/<int:pk>/', CourseDetail.as_view()),

	path('units/', UnitList.as_view()),
	path('units/<int:pk>/', UnitDetail.as_view()),

	path('lectures/', LectureList.as_view()),
	path('lectures/<int:pk>/', LectureDetail.as_view()),

	path('course-members/', CourseMemberList.as_view()),
	path('course-members/<int:pk>/', CourseMemberDetail.as_view()),

	path('categories/', CategoryList.as_view()),
	path('categories/<int:pk>/', CategoryDetail.as_view()),

	path('articles/', ArticleList.as_view()),
	path('articles/<int:pk>/', ArticleDetail.as_view()),

	path('practices/', PracticeList.as_view()),
	path('practices/<int:pk>/', PracticeDetail.as_view()),
] 

# urlpatterns += router.urls
