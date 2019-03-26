import sys 
from django.conf import settings
from django.urls import path 
from django.http import HttpResponse
from django.core.management import execute_from_command_line

settings.configure(
	DEBUG=True,
    ROOT_URLCONF =__name__,
	)
	
def index(request):
	return HttpResponse('Hello, world')

urlpatterns = (
	path('', index),
	)

execute_from_command_line(sys.argv)