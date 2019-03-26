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


class ItemBase(models.Model):
	title = models.CharField(max_length=127, verbose_name=_('الاسم'))
	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الاضافة"))
	updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخر تعديل في"))


	class Meta:
		abstract = True

	def __str__(self):
		return str(self.title)


class Text(ItemBase):
	content = models.TextField(verbose_name=_('المحتوي'))
	class Meta:
		verbose_name = _("نص")
		verbose_name_plural = _("المحتوي النصي")

class File(ItemBase):
	file = models.FileField(upload_to='content/files', verbose_name=_('الملف'))
	class Meta:
		verbose_name = _("ملف")
		verbose_name_plural = _("الملفات")

class Image(ItemBase):
	file = models.ImageField(upload_to='content/images/%Y/%m/%d', blank=True, verbose_name=_('صورة'))
	class Meta:
		verbose_name = _("صورة")
		verbose_name_plural = _("الصور")

class Video(ItemBase):
	url = models.URLField(verbose_name=_('العنوان'))
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
	
	title = models.CharField(max_length=127, verbose_name=_('الاسم'))
	content = models.TextField(blank=True, verbose_name=_('المحتوي'))
	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الاضافة"))
	updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخر تعديل في"))
	slug = models.SlugField(db_index=True, unique=True)
	status = models.CharField(max_length=10, choices = STATUS_CHOICES, default='published', verbose_name=_("الحالة"))
	publish = models.DateTimeField(default=now, verbose_name=_("تاريخ النشر"))
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

	overview = models.TextField(blank=True, verbose_name=_('المقدمة'))
	image = models.ImageField(upload_to='courses/img/%Y/%m/%d', blank=True, verbose_name=_('صورة'))

	# V 2.
	# CRSPrice =
	# CRSPoint =

	profile  = models.ManyToManyField(Profile, related_name='courses', through='CourseMember', verbose_name=_("المستخدمين"))

	class Meta:
		ordering = ('-created_at',)
		verbose_name = _("كورس")
		verbose_name_plural = _("كورسات")

	def get_absolute_url(self):
		return reverse('track:course', kwargs={'slug': self.slug})


class Unit(TrackBase):

	course = models.ForeignKey(Course, related_name='units', on_delete=models.CASCADE, verbose_name=_("الكورس"))
	img = models.ImageField(upload_to='courses/unit/img/%Y/%m/%d', blank=True, verbose_name=_('صورة'))
	# from our custom field
	order = OrderField(blank=True, for_fields=['course'])

	def __str__(self):
		return '{}. {}'.format(self.order, self.title)

	class Meta:
		ordering = ['order']
		verbose_name = _("الوحدة")
		verbose_name_plural = _("الوحدات")

	def get_absolute_url(self):
		return reverse('track:unit', args=[self.slug])


class Content(models.Model):
	unit = models.ForeignKey(Unit, related_name='contents', on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
		limit_choices_to={'model__in':('text', 'video', 'image', 'file')}) 
	object_id = models.PositiveIntegerField()
	item = GenericForeignKey('content_type', 'object_id')
	order = OrderField(blank=True, for_fields=['unit'])

	class Meta:
		ordering = ['order']


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
	views = models.PositiveIntegerField(default=0,  verbose_name=_("المشاهدات"))
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


class Practice(TrackBase):

	category = models.ForeignKey(Category, related_name='practices', on_delete=models.CASCADE, verbose_name=_('القسم'))
	
	class Meta:
		verbose_name = _("تمرين")
		verbose_name_plural = _("التمارين") # s

	# def get_absolute_url(self):
	#   return reverse('track:practice-detail', args=[self.PRASlug])


class Track(TrackBase):

	courses  = models.ManyToManyField(Course, related_name='track', verbose_name=_("الكورسات"))
	articles  = models.ManyToManyField(Article, related_name='track', verbose_name=_("مقالات"))
	practices  = models.ManyToManyField(Practice, related_name='track', verbose_name=_("تمارين"))

	image = models.ImageField(upload_to='tracks/img/%Y/%m/%d', blank=True, verbose_name=_('صورة'))

	# V3.x
	# User  = models.ManyToManyField(User, verbose_name=_("المدرسين"))

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