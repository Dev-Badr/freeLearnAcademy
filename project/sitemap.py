from django.contrib.sitemaps import Sitemap
from track.models import *

class TrackSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Track.published.all()

    def lastmod(self, obj):
        return obj.publish