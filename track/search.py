from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.db.models import Q
from .forms import SearchForm
from .models import Article, Course

@csrf_protect
def article_search(request):

	cd = request.POST['q']

	articles = None

	if cd == "":
		articles = Article.published.all()
	else:
		articles = Article.published.filter(
			Q(title__icontains=cd) |
			Q(content__icontains=cd) |
			Q(publish__icontains=cd)).all()

	total_results = articles.count()
	print(articles)
	context = {
		'articles':articles,
		'total_results':total_results,
		'cd':cd,
	}

	return render(request, 'track/search/article_search.html', context)

@csrf_protect
def course_search(request):

	cd = request.POST['q']
	courses = None

	if cd == "":
		courses = Course.published.all()
	else:
		courses = Course.published.filter(
			Q(title__icontains=cd) |
			Q(content__icontains=cd) |
			Q(publish__icontains=cd)).all()

	total_results = courses.count()
	context = {
		'courses':courses,
		'total_results':total_results,
		'cd':cd,
	}

	return render(request, 'track/search/course_search.html', context)