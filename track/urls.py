from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *
from .search import article_search, course_search

app_name = 'track'

urlpatterns = [
    
    # SEARCH
    # v.4x we must search in also specific category and tag
    # path('courses/search', search_track, name='course_search'),
    # path('users/search', search_track, name='user_search'),

	# tracks
    path('tracks/', TrackView.as_view(), name='track-list'),
    path('tracks/<slug:slug>/', TrackDetailView.as_view(), name='track-detail'),

    # courses
    path('courses/', CourseView.as_view(), name='course-list'),
    #ajax search
    path('courses/search', course_search, name='course_search'),

    # my courses
    path('account/dashboard', DashboardView.as_view(), name='dashboard'),

    # course detail
    path('courses/<slug:slug>/', 
            CourseDetailView.as_view(), name='course-detail'),

    #join or leave track
    path('course/<slug:slug>/join', JoinCourse.as_view(), name='join'),
    path('course/<slug:slug>/leave', LeaveCourse.as_view(), name='leave'),

    ############################ articles #############################

    # All
    path('articles/', ModelListView.as_view(model=Article), name='article-list'),
    
    #ajax search
    path('articles/search', article_search, name='article_search'),

    # articles by track_slug
    path('<slug:track_slug>/articles', login_required(
            ModelListView.as_view(model=Article)), name='article_list_by_track'),

    # articles by category_slug
    path('articles/category/<slug:category_slug>', login_required(
            ModelListView.as_view(model=Article)),
            name='article_list_by_category'),

    # articles by tag_slug
    path('articles/tag/<slug:tag_slug>', login_required(
            ModelListView.as_view(model=Article)), name='article_list_by_tag'),
    
    # Detail
    path('article/<int:id>/<slug:slug>', 
            ArticleDetailView.as_view(model=Article), name='article-detail'),

    ########################### practices #############################

    # practices
    path('practices/', ModelListView.as_view(
                        model=Practice), name='practice-list'),

    path('<slug:track_slug>/practices', login_required(
            ModelListView.as_view(model=Practice)), name='practice_list_by_track'),
    
    path('practices/category/<slug:category_slug>', login_required(
            ModelListView.as_view(model=Practice)), name='practice_list_by_category'),

    # practice detail
    path('practices/<slug:slug>', 
            PracticeDetailView.as_view(), name='practice-detail'),

    ####################################################################
    

     ##################################################################
    #---------------------------Site-Maps------------------------------#
    # path(r'sitemap\.xml', sitemap,                                   #
    #         {'sitemaps': sitemaps},                                  #
    #             name='django.contrib.sitemaps.views.sitemap'),       #
     ##################################################################


    # those urls must be in the buttom
    # units    
    path('<slug:course_slug>/<slug:slug>',
            UnitDetailView.as_view(), name='unit-detail'),
    # lectures
    path('<slug:course_slug>/<slug:slug>/<slug:lecture_slug>', 
            UnitDetailView.as_view(), name='lecture-detail'),

    # path('<slug:course_slug>/<slug:slug>', RedirectView.as_view(
    #         url=reverse_lazy('track:lecture-detail')), name='unit-detail' ),

]


# Create fake data
    # path('create_users/<int:number>', create_users, name='create_users'),
    # path('create_videos/<int:number>', create_videos, name='create_items'),
    # path('create_category/<int:number>', create_category, name='create_category'),
