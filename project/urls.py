"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _

# SiteMaps

# from django.contrib.sitemaps.views import sitemap
# from .sitemap import TrackSitemap

# sitemaps = {
#     'tracks': TrackSitemap,
#     # 'courses': CourseSitemap,
#     # 'articles': ArticleSitemap,
#     # 'practices': PracticeSitemap,
# }




handler404 = 'track.handle_errors.handler404'

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),

    # all auth
    # path('auth/', include('allauth.urls')),
    path('', include('home.urls', namespace='home')),
    path('api/v1/', include('track.api.urls', namespace='api-track')),
    path('', include('track.urls', namespace='track')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # -Site-Maps- #
    # path(r'sitemap\.xml', sitemap,
    #         {'sitemaps': sitemaps}, 
    #             name='django.contrib.sitemaps.views.sitemap'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = _(" freeLearnAcademy Admin Panel")
admin.site.site_title =_( " freeLearnAcademy App Admin")
admin.site.site_index_title = _(" Welcome To freeLearnAcademy Admin Panel")
