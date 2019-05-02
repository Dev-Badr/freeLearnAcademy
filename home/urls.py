from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'home'

urlpatterns = [
	path('', home, name='home'),
	path('search/', home_search, name='search'),
	path('search-results/', search_results, name='search-results'),
]
