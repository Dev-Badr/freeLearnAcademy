from django import template
register = template.Library()
from ..models import *

@register.simple_tag
def total_tracks():
    return Track.published.count()

@register.simple_tag
def total_courses():
    return Course.published.count()

@register.simple_tag
def total_practices():
    return Practice.published.count()

@register.simple_tag
def total_articles():
	# need to /10 to get by 10 articles
	# ex: 20 30 40 .. ect.
    return Article.published.count()
