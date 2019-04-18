from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from accounts.models import Profile
from django.utils.text import slugify
from project.utils import get_current_site
from taggit.managers import TaggableManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField # custom field
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class ItemBase(models.Model):
	title = models.CharField(_('الاسم'), max_length=127)
	created_at = models.DateTimeField(_("تاريخ الاضافة"), auto_now_add=True)
	updated_at = models.DateTimeField(_("آخر تعديل في"), auto_now=True)

	def render(self):
		return render_to_string('track/content/{}.html'.format(
				   self._meta.model_name), {'item': self})

	class Meta:
		abstract = True

	def __str__(self):
		return str(self.title)


class Text(ItemBase):
	content = models.TextField(_('المحتوي'))
	class Meta:
		verbose_name = _("نص")
		verbose_name_plural = _("النصوص")

class File(ItemBase):
	file = models.FileField(_('الملف'), upload_to='content/files')
	class Meta:
		verbose_name = _("ملف")
		verbose_name_plural = _("الملفات")

class Image(ItemBase):
	file = models.ImageField(_('صورة'), upload_to='content/images/%Y/%m/%d', blank=True)
	class Meta:
		verbose_name = _("صورة")
		verbose_name_plural = _("الصور")

class Video(ItemBase):
	url = models.URLField(_('العنوان'))
	class Meta:
		verbose_name = _("فديو")
		verbose_name_plural = _("الفديوهات")


## Filter Manager
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,  
						self).get_queryset()\
							.filter(status='published')

STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
	)

class TrackBase(models.Model):
	
	title = models.CharField(_('الاسم'), max_length=127)
	content = models.TextField(_('المحتوي'), blank=True)
	created_at = models.DateTimeField(_("تاريخ الاضافة"), auto_now_add=True)
	updated_at = models.DateTimeField(_("آخر تعديل في"), auto_now=True)
	slug = models.SlugField(db_index=True, unique=True)
	status = models.CharField(_("الحالة"), max_length=10, choices = STATUS_CHOICES, default='published')
	publish = models.DateTimeField(_("تاريخ النشر"), default=now)
	objects = models.Manager()
	published = PublishedManager()

	class Meta:
		abstract = True

	def __str__(self):
		return str(self.title)

	def save(self , *args , **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	def get_full_url(self):
		site = get_current_site().domain
		url = "https://{site}{path}".format(site=site, path=self.get_absolute_url())
		return url

#######

class Course(TrackBase):

	overview = models.TextField(_('المقدمة'), blank=True)
	# image = models.ImageField(_('صورة'), upload_to='courses/img/%Y/%m/%d', blank=True)
	joines = models.PositiveIntegerField(_("اجمالي المنضمون"), default=0)

	# V 3.x
	# CRSPrice =
	# CRSPoint =
	# profile_complete
	
	profile  = models.ManyToManyField(Profile, related_name='courses', through='CourseMember', verbose_name=_("المستخدمين"))

	class Meta:
		ordering = ('-created_at',)
		verbose_name = _("كورس")
		verbose_name_plural = _("كورسات")

	def joined(self):
		self.joines += 1
		self.save(update_fields=['joines'])

	def get_absolute_url(self):
		return reverse('track:course-detail', kwargs={'slug': self.slug})


class Unit(TrackBase):

	course = models.ForeignKey(Course, related_name='units', on_delete=models.CASCADE, verbose_name=_("الكورس"))
	# image = models.ImageField(_('صورة'), upload_to='courses/unit/img/%Y/%m/%d', blank=True)
	last_lecture = models.PositiveIntegerField(blank=True, null=True)
	# order field can't tack verbose-name 1st argument
	order = OrderField(blank=True, for_fields=['course'], verbose_name=_('الترتيب'))

	def __str__(self):
		return '{}. {}'.format(self.order, self.title)

	class Meta:
		ordering = ['order']
		verbose_name = _("الوحدة")
		verbose_name_plural = _("الوحدات")

	# save id for last_lecture user entered
	def entered(self, lecture_id):
		self.last_lecture = lecture_id
		self.save(update_fields=['last_lecture'])

	def get_absolute_url(self):
		return reverse('track:unit-detail', kwargs={
				'course_slug':self.course.slug , 'slug': self.slug})


class Lecture(TrackBase):
	unit = models.ForeignKey(Unit, related_name='lectures', on_delete=models.CASCADE, verbose_name=_('الوحدة'))
	views = models.PositiveIntegerField(_("المشاهدات"), default=0)
	order = OrderField(blank=True, for_fields=['unit'], verbose_name=_('الترتيب'))


	def __str__(self):
		return '{}. {}'.format(self.order, self.title)

	class Meta:
		ordering = ['order']
		verbose_name = _("محاضرة")
		verbose_name_plural = _("المحاضرات")

	def viewed(self):
		self.views += 1
		self.save(update_fields=['views'])

	def get_absolute_url(self):
		return reverse('track:lecture-detail', kwargs={
			'course_slug':self.unit.course.slug,
			'slug': self.unit.slug,
			'lecture_slug': self.slug})



class Content(models.Model):
	lecture = models.ForeignKey(Lecture, related_name='contents', on_delete=models.CASCADE, verbose_name=_('المحاضرة'))
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
		limit_choices_to={'model__in':('text', 'video', 'image', 'file')}, verbose_name=_('النوع')) 
	object_id = models.PositiveIntegerField()
	item = GenericForeignKey('content_type', 'object_id')
	order = OrderField(blank=True, for_fields=['lecture'], verbose_name=_('الترتيب'))

	class Meta:
		ordering = ['order']
		verbose_name = 'محتوي'
		verbose_name_plural = 'المحتويات'

	def __str__(self):
		return str(self.content_type)


class Category(ItemBase):

	slug = models.SlugField(db_index=True, unique=True)

	def save(self , *args , **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super(Category, self).save( *args , **kwargs)

	class Meta:
		ordering = ('title', )
		verbose_name = 'القسم'
		verbose_name_plural = 'الاقسام'

	# def get_absolute_url(self):
	#   return reverse('track:article_list_by_category', args=[self.slug])


class Article(TrackBase):

	category = models.ForeignKey(Category, related_name='articles', on_delete=models.CASCADE, verbose_name=_('القسم'))
	views = models.PositiveIntegerField(_("المشاهدات"), default=0)
	tags = TaggableManager()

	class Meta:
		verbose_name = _("مقال")
		verbose_name_plural = _("المقالات") # s


	def get_absolute_url(self):
		return reverse('track:article-detail', 
							kwargs={'id':self.id, 'slug':self.slug})

	def viewed(self):
		self.views += 1
		self.save(update_fields=['views'])


# class Vote(models.Model):
#     article = models.ForeignKey(to=Article)
#     voter = models.ForeignKey(to=User, related_name='voter')
#     timestamp = models.DateTimeField(auto_now_add=True)

# Article.objects.filter(tags=tag).\
#    annotate(vote_count=Count('vote')).order_by('-vote_count')

# Article.objects.filter(tags=tag).\
# 	annotate(favorite_count=Count('user')).order_by('-favorite_count')


class Practice(TrackBase):

	category = models.ForeignKey(Category, related_name='practices', on_delete=models.CASCADE, verbose_name=_('القسم'))
	
	class Meta:
		verbose_name = _("تمرين")
		verbose_name_plural = _("التمارين") # s

	def get_absolute_url(self):
	  return reverse('track:practice-detail', kwargs={
	  	'slug':self.slug})


class Track(TrackBase):

	courses  = models.ManyToManyField(Course, related_name='track', verbose_name=_("الكورسات"))
	articles  = models.ManyToManyField(Article, related_name='track', verbose_name=_("مقالات"))
	practices  = models.ManyToManyField(Practice, related_name='track', verbose_name=_("تمارين"))

	# image = models.ImageField(_('صورة'), upload_to='tracks/img/%Y/%m/%d', blank=True)

	class Meta:
		verbose_name = _("مسار")
		verbose_name_plural = _("مسارات") # s

	def get_absolute_url(self):
		return reverse('track:track-detail', args=[self.slug])


class CourseMember(models.Model):
	course = models.ForeignKey(Course, related_name='memberships', on_delete=models.CASCADE)
	profile = models.ForeignKey(Profile, related_name='members', on_delete=models.CASCADE)

	def __str__(self):
		return self.profile.user.username

	class Meta:
		unique_together = ('course', 'profile')
		verbose_name = _("عضو مشترك")
		verbose_name_plural = _("المشتركين")


# class CourseComplete(models.Model):
# 	course = models.ForeignKey(Course, related_name='completer', on_delete=models.CASCADE)
# 	profile = models.ForeignKey(Profile, related_name='completer', on_delete=models.CASCADE)

# 	def __str__(self):
# 		return self.profile.user.username

# 	class Meta:
# 		unique_together = ('course', 'profile')
# 		verbose_name = _("عضو مشترك")
# 		verbose_name_plural = _("المشتركين")