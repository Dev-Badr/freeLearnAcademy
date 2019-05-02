from django.db import models
from django.urls import reverse
from django.conf import settings
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


PREV_LANGUAGES = (
	('py', 'Python'), ('c', 'C'), ('c++', 'C++'),
	('c#', 'C#'), ('VB', 'VB.NET'), ('ruby', 'Ruby'),
	('java', 'Java'), ('js', 'JavaScript'), ('php', 'Php'),
	('django', 'Django'), ('flask', 'Flask'), ('ror', 'RubyOnRails'),
	('html', 'HTML'), ('css', 'CSS'), ('bootstrap', 'BootStrap'),
	('react', 'React'), ('angular', 'Angular'), ('ring', 'Ring'),
)

class Profile(models.Model):

	GENDER = (('male', 'رجل'), ('female', 'امرأه'))

	user   = models.OneToOneField(
		User, related_name='profile', on_delete=models.CASCADE
	)

	views  = models.PositiveIntegerField(_("المشاهدات"), default=0)
	photo  = models.ImageField(
		_('صورة'), upload_to='users/img/profile/%Y/%m/%d', blank=True
	)

	# points = models.PositiveIntegerField(_("النقاط"), default=0)

	bio    = models.TextField(
		_('نبذة تعريفية'), max_length=99, blank=True, null=True
	)

	gender = models.CharField(_('النوع'), max_length=6, choices=GENDER)
	mobile = models.CharField(
		_("رقم الهاتف"), max_length=20, blank=True, null=True
	)

	date_of_birth = models.DateField(
		_('تاريخ الميلاد'), blank=True, null=True
	)

	facebook = models.CharField(
		_("فيسبوك"), max_length=100, blank=True, null=True
	)

	twitter= models.CharField(
		_("تويتر"), max_length=100, blank=True, null=True
	) 

	github = models.CharField(
		_("جيت هب"), max_length=100, blank=True, null=True
	) 

	whatsapp_mobile = models.CharField(
		_(" رقم الهاتف واتس اب"), max_length=20, blank=True, null=True
	) 

	prev_languages = models.CharField(
		_('اللغة المفضلة'), max_length=8, choices=PREV_LANGUAGES
	)

	read_articles = models.PositiveIntegerField(_("قرآءةالمقالات"), default=0)
	last_lecture  = models.PositiveIntegerField(blank=True, null=True)
	
	class Meta:
		verbose_name = _("الصفحة الشخصية")
		verbose_name_plural = _("الصفحات الشخصية")

	def viewed(self):
		self.views += 1
		self.save(update_fields=['views'])

	# def read_article(self, article_id):
	# 	self.read_articles = article_id
	# 	self.save(update_fields=['read_articles'])

	# save id for last_lecture user entered
	def entered(self, lecture_id):
		self.last_lecture = lecture_id
		self.save(update_fields=['last_lecture'])

	# def loged(self):
	# 	self.last_seen = now()
	# 	self.save(update_fields=['last_seen'])

	def __str__(self):
		return 'Profile for user {}'.format(self.user.username)

	def get_absolute_url(self):
		return reverse('accounts:users', kwargs={
				'username':self.user.username
			}
		)


@receiver(post_save,sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()