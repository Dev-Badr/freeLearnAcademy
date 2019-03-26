from django.contrib.sites.models import Site

def get_current_site():
    site = Site.objects.get_current()
    return site