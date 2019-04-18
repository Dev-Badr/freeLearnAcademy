from .models import *
from django.http import HttpResponse
from django.views.generic import View, RedirectView, TemplateView
from django.contrib import messages
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Count
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from accounts.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.contrib.auth.mixins import LoginRequiredMixin

class TrackView(ListView):
	model = Track

class TrackDetailView(DetailView):
	model = Track

class CourseView(ListView):
	model = Course

class DashboardView(LoginRequiredMixin, ListView):
	model = Course
	template_name = 'accounts/dashboard.html'

	def get_queryset(self):
		qs = super(DashboardView, self).get_queryset()
		return qs.filter(profile__in=[self.request.user.profile])

	def get_context_data(self, **kwargs):
		context = super(DashboardView, self).get_context_data(**kwargs)
		lecture_id = self.request.user.profile.last_lecture
		# when user leave the course 
		if lecture_id:
			context['lecture'] = Lecture.objects.get(id=lecture_id)

		return context


class CourseDetailView(DetailView):
	model = Course

class UnitDetailView(LoginRequiredMixin, DetailView):
	model = Unit

	# check if user enrolled in this course or not
	def dispatch(self, request, *args, **kwargs):
		profile = self.request.user.profile
		if not profile.courses.filter(profile=profile):
			messages.warning(
				self.request, "Please register first to be able to access the content of the course.")

			return redirect("track:course-detail", slug=self.kwargs.get("course_slug"))
		return super(UnitDetailView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		course = get_object_or_404(Course, slug=self.kwargs.get("course_slug"))

		profile = self.request.user.profile

		context = super(UnitDetailView, self).get_context_data(**kwargs)
		unit = get_object_or_404(Unit, slug=self.kwargs.get('slug'))
		lecture_slug = self.kwargs.get("lecture_slug")
		lecture = None

		if lecture_slug:
			lecture = unit.lectures.filter(slug=lecture_slug)[0]
			unit.entered(lecture.id)
			profile.entered(lecture.id)
		else:
			# get the last lecture id.
			lecture_id = unit.last_lecture
			# The first time user entered the unit will redirect to introduction to module
			if lecture_id:
				lecture =  unit.lectures.get(id=lecture_id)
		lecture.viewed()
		context['unit'] = unit
		context['lecture'] = lecture

		return context
		

# JOIN THE TRACK
class JoinCourse(LoginRequiredMixin, RedirectView):

	def get_redirect_url(self, *args, **kwargs):

		return reverse("track:course-detail",
					kwargs={"slug": self.kwargs.get("slug")})

	def get(self, request, *args, **kwargs):
		course = get_object_or_404(Course,
						slug=self.kwargs.get("slug"))
		try:
			CourseMember.objects.create(
				profile=self.request.user.profile, course=course)
			
			course.joined()

		except IntegrityError:
			messages.warning(self.request,(
				"You are already a member of {}.".format(course.title)))
		else:
			messages.success(self.request,
				"You are now a member of {}.".format(course.title))

		return super().get(request, *args, **kwargs)

# LEAVE THE TRACK
class LeaveCourse(LoginRequiredMixin, RedirectView):

	def get_redirect_url(self, *args, **kwargs):
		return reverse("track:dashboard")

	def get(self, request, *args, **kwargs):
		profile = self.request.user.profile
		try:
			membership = CourseMember.objects.filter(
				profile=profile,
				course__slug=self.kwargs.get("slug")).get()

			# logic : if user remove any course 
			# "complete your last lecture" not work
			profile.entered(None)
		except CourseMember.DoesNotExist:
			messages.warning(
				self.request, "You are not registered in this course."
			)
		else:
			membership.delete()
			messages.success(
				self.request, "You successfully left the course."
			)
		return super().get(request, *args, **kwargs)

# this class handel two models (Article, Practice)
class ModelListView(ListView):

	model = None
	paginate_by = 5

	def get_context_data(self, **kwargs):

		context = super(ModelListView, self).get_context_data(**kwargs)

		# By default context articles are sent when we assign variable model = article
		# But we do not want to make a complex HTML file
		# We make one loop "for 2 models" (Article, Practice)

		my_object_list = self.model.published.all()
		context['categories'] = Category.objects.all()

		# Most popular tags
		context['tags'] = Tag.objects.\
			annotate(num=Count('taggit_taggeditem_items')).order_by('-num')[:10]

		# 3 variables for specific articles
		track_slug = self.kwargs.get("track_slug")
		category_slug = self.kwargs.get("category_slug")
		tag_slug = self.kwargs.get("tag_slug")

		if track_slug:
			track = get_object_or_404(Track, slug=track_slug)
			my_object_list = self.model.published.filter(track=track).all()

		if category_slug:
			category = get_object_or_404(Category, slug=category_slug)
			my_object_list = self.model.published.filter(category=category).all()

			# To find out what category is active
			context['category'] = category

		if tag_slug:
			tag =  get_object_or_404(Tag, slug=tag_slug)
			my_object_list = Article.published.filter(tags=tag).all()

			# To find out what category is active
			context['tag'] = tag

		context['my_object_list'] = my_object_list

		return context


class ArticleDetailView(LoginRequiredMixin, DetailView):

	model = Article
 
	# user can reads 2000 articles
	# even we have just 1 article by refresh the page

	# def get(self, request, *args, **kwargs):
	#     profile = self.request.user.profile
	#     profile.read_article()
	#     return super(ArticleDetailView, self).get(request, *args, **kwargs)

	def get_object(self, queryset=None):
		obj = super(ArticleDetailView, self).get_object()
		obj.viewed()
		self.object = obj
		return obj

	def get_context_data(self, **kwargs):
		context = super(ArticleDetailView, self).get_context_data(**kwargs)
		article = get_object_or_404(Article,
			id=self.kwargs.get("id"), slug=self.kwargs.get("slug"),
			status='published')

		# List of similar Articles
		article_tags_ids = article.tags.values_list('id', flat=True)
		similar_articles = Article.published.filter(
								tags__in=article_tags_ids)\
									.exclude(id=article.id)

		context['similar_articles'] = similar_articles.annotate(
										same_tags=Count('tags'))\
											.order_by('-same_tags','-created_at')[:3]
		return context


class PracticeDetailView(LoginRequiredMixin, DetailView):
	model = Practice
	

# ERROR-PAGE
# def page_not_found_view(request, exception, template_name='error_page.html'):
#     if exception:
#         logger.error(exception)
#     url = request.get_full_path()
#     return render(request, template_name,
#                   {'message': 'no url match' + url , 'statuscode': '404'}, status=404)