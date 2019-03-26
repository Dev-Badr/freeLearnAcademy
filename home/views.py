from django import forms
from django.shortcuts import render, redirect
from .forms import HomeRegisterForm
from accounts.models import Profile
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from track.forms import SearchForm
from track.models import Track, Article, Course

@csrf_protect
def home(request):
    if request.user.is_authenticated:
        context = {'tracks': Track.published.all(),
                    'articles': Article.published.all()\
                    .order_by('-created_at')[:3]}
        return render(request, 'home/home_log.html', context)

    else:
        if request.method == 'POST':
            form = HomeRegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email =  form.cleaned_data['email']
                password =  form.cleaned_data['password']
                if not (User.objects.filter(
                    username=username).exists() or User.objects.filter(
                    email=email).exists()):
                    User.objects.create_user(username, email, password)
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect('accounts:edit_account')
                #need validation here
        else:
            form = HomeRegisterForm()
        users = User.objects.count()
        return render(request, 'home/home.html', {'form' : form, 'users':users})



def home_search(request):
    return render(request, 'home/search.html')

@csrf_protect
def search_results(request):

    cleandata = request.POST['q']
    users = None
    courses = None
    articles = Article.published.filter(
        Q(title__icontains=cleandata) |
        Q(content__icontains=cleandata) |
        Q(publish__icontains=cleandata)).all()

    courses = Course.published.filter(
        Q(title__icontains=cleandata) |
        Q(content__icontains=cleandata) |
        Q(publish__icontains=cleandata)).all()

    users = User.objects.filter(
        Q(username__icontains=cleandata)).all()

    total_results = articles.count() + \
        courses.count() + users.count()

    context = {
        'articles':articles,
        'cleandata':cleandata,
        'total_results':total_results,
        'courses':courses, 'users':users,
    }
    return render(request, 'home/search_results.html', context)



# class HomeSearch(View):

#     template_name = 'home/search.html'

#     def get(self, request, *args, **kwargs):

#         cleandata = ''
#         articles = None
#         users = None
#         courses = None
#         total_results = 0

#         form = SearchForm()
#         if 'query' in request.GET:
#             form = SearchForm(request.GET)
#             if form.is_valid():
#                 cleandata = form.cleaned_data['query']

#                 articles = Article.published.filter(
#                     Q(title__icontains=cleandata) |
#                     Q(content__icontains=cleandata) |
#                     Q(publish__icontains=cleandata)).all()

#                 courses = Course.published.filter(
#                     Q(title__icontains=cleandata) |
#                     Q(content__icontains=cleandata) |
#                     Q(publish__icontains=cleandata)).all()

#                 users = User.objects.filter(
#                     Q(username__icontains=cleandata)).all()

#                 total_results = articles.count() + \
#                 courses.count() + users.count()

#         context = {'form': form, 'users':users, 'articles':articles,
#                     'cleandata':cleandata, 'total_results':total_results, 'courses':courses}

#         return render(request, self.template_name, context)
