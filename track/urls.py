from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *
from .search import article_search, course_search

app_name = 'track'

urlpatterns = [
    
    # v.4x We must search in a category and a specific tag as well
    
	# Tracks
    path('tracks/', TrackView.as_view(), name='track-list'),

    # Track Detail
    path('tracks/<slug:slug>/', TrackDetailView.as_view(),
        name='track-detail'
    ),

    # Courses
    path('courses/', CourseView.as_view(), name='course-list'),

    # Ajax search
    path('courses/search', course_search, name='course_search'),

    # My courses
    path('account/dashboard', DashboardView.as_view(), name='dashboard'),

    # Course detail
    path('courses/<slug:slug>/', CourseDetailView.as_view(), 
        name='course-detail'
    ),

    # Join the track
    path('course/<slug:slug>/join', JoinCourse.as_view(), name='join'),

    # Leave the track
    path('course/<slug:slug>/leave', LeaveCourse.as_view(), name='leave'),

    ############################ articles #############################

    # Whole articles
    path('articles/', ModelListView.as_view(model=Article), 
        name='article-list'
    ),
    
    # ajax search
    path('articles/search', article_search, name='article_search'),

    # articles from a particular track
    path('<slug:track_slug>/articles', login_required(
        ModelListView.as_view(model=Article)), 
        name='article_list_by_track'
    ),

    # articles from a particular category
    path('articles/category/<slug:category_slug>', login_required(
        ModelListView.as_view(model=Article)),
        name='article_list_by_category'
    ),

    # articles from a particular tag
    path('articles/tag/<slug:tag_slug>', login_required(
        ModelListView.as_view(model=Article)), 
        name='article_list_by_tag'
    ),
    
    # track detail
    path('article/<int:id>/<slug:slug>', 
        ArticleDetailView.as_view(model=Article), 
        name='article-detail'
    ),

    ########################### practices #############################

    # Whole articles
    path('practices/', ModelListView.as_view(
        model=Practice), name='practice-list'
    ),

    # Practices from a particular track
    path('<slug:track_slug>/practices', login_required(
        ModelListView.as_view(model=Practice)), 
        name='practice_list_by_track'
    ),
    
    # Practices from a particular category
    path('practices/category/<slug:category_slug>', login_required(
        ModelListView.as_view(model=Practice)), 
        name='practice_list_by_category'
    ),

    # Practice detail
    path('practices/<slug:slug>', 
        PracticeDetailView.as_view(), name='practice-detail'
    ),


     ##############################################################
    #---------------------------Site-Maps-------------------------#
    # path(r'sitemap\.xml', sitemap,                              #
    #         {'sitemaps': sitemaps},                             #
    #             name='django.contrib.sitemaps.views.sitemap'),  #
     ##############################################################

    # Course modules    
    path('<slug:course_slug>/<slug:slug>',
        UnitDetailView.as_view(), name='unit-detail'
    ),
    # lectures
    path('<slug:course_slug>/<slug:slug>/<slug:lecture_slug>', 
        UnitDetailView.as_view(), name='lecture-detail'
    ),
]