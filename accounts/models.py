from django.db import models
from django.urls import reverse
from django.conf import settings
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


# COUNTRIES = (
# 	('eg', _('مصر'), ('sa', 'السعودية'), ('ma', 'المغرب'),
# 	)

PREVLANGUAGES = (
	('py', 'Python'), ('c', 'C'), ('c++', 'C++'),
	('c#', 'C#'), ('VB', 'VB.NET'), ('ruby', 'Ruby'),
	('java', 'Java'), ('js', 'JavaScript'), ('php', 'Php'),
	('django', 'Django'), ('flask', 'Flask'), ('ror', 'RubyOnRails'),
	('html', 'HTML'), ('css', 'CSS'), ('bootstrap', 'BootStrap'),
	('react', 'React'), ('angular', 'Angular'), ('ring', 'Ring'),
	)

class Profile(models.Model):

	GENDER = (('male', 'رجل'), ('female', 'امرأه'))

	user   = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
	views  = models.PositiveIntegerField(_("المشاهدات"), default=0)
	photo  = models.ImageField(_('صورة'), upload_to='users/img/profile/%Y/%m/%d', blank=True)
	# contry = models.CharField(_('الدولة'), max_length=10, choices = COUNTRIES)
	# points = models.PositiveIntegerField(_("النقاط"), default=0)
	bio    = models.TextField(_('نبذة تعريفية'), max_length=99, blank=True, null=True)
	gender = models.CharField(_('النوع'), max_length=6, choices = GENDER)
	mobile = models.CharField(_("رقم الهاتف"), max_length=20, blank=True, null=True)
	date_of_birth   = models.DateField(_('تاريخ الميلاد'), blank=True, null=True)
	facebook  	    = models.CharField(_("فيسبوك"), max_length=100, blank=True, null=True)
	twitter    		= models.CharField(_("تويتر"), max_length=100, blank=True, null=True) 
	github   		= models.CharField(_("جيت هب"), max_length=100, blank=True, null=True) 
	whatsapp_mobile = models.CharField(_(" رقم الهاتف واتس اب"), max_length=20, blank=True, null=True) 
	prev_languages  = models.CharField(_('اللغة المفضلة'), max_length=8, choices = PREVLANGUAGES)
	read_articles   = models.PositiveIntegerField(_("قرآءةالمقالات"), default=0)
	last_lecture    = models.PositiveIntegerField(blank=True, null=True)
	
	# solve_ex

	# we should make another one model for courses completed
	# and make 2 relationships for course name and profile user

	# 

	# admin do that on field > user.last_login
	# last_seen = models.DateTimeField(_('آخر مشاهدة'), default=now)
	
	class Meta:
		verbose_name = _("الصفحة الشخصية")
		verbose_name_plural = _("الصفحات الشخصية")

	def viewed(self):
		self.views += 1
		self.save(update_fields=['views'])

	# def read_article(self):
	# 	self.read_articles += 1
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
		return reverse('accounts:users', kwargs={'username':self.user.username})


@receiver(post_save,sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


#########################################

# from django.contrib.auth.models import AbstractBaseUser

# class MyUser(AbstractBaseUser):

# 	email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
# 	date_of_birth = models.DateField()
# 	is_active = models.BooleanField(default=True)
# 	is_admin = models.BooleanField(default=False)

# 	USERNAME_FIELD = 'email'
# 	REQUIRED_FIELDS = ['email']

# 		return self.is_admin
# 	def __str__(self):
# 		return self.email

# 	def has_perm(self, perm, obj=None):
# 		"Does the user have a specific permission?"
# 		# Simplest possible answer: Yes, always
# 		return True

# 	def has_module_perms(self, app_label):
# 		"Does the user have permissions to view the app `app_label`?"
# 		# Simplest possible answer: Yes, always
# 		return True

# 	@property
# 	def is_staff(self):
# 		"Is the user a member of staff?"
# 		# Simplest possible answer: All admins are staff