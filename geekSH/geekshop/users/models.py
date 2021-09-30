from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class NormalUser(AbstractUser):
	image = models.ImageField(upload_to="users_images", blank=True)
	age = models.PositiveIntegerField(verbose_name="age", default=18)
	email = models.EmailField(verbose_name='email address', blank=True, unique=True)

	activation_key = models.CharField(max_length=128, blank=True)
	activation_key_expires = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	# activation_key_expires = models.DateTimeField(default=now()+timedelta(hours=48))

	def is_activation_key_expired(self):
		if now() <= self.activation_key_expires + timedelta(hours=48):
			return False
		return True

class UserProfile(models.Model):
	MALE = "M"
	FEMALE = "W"
	GENDER_CHOICES = ((MALE, "М"), (FEMALE, "Ж"))

	user = models.OneToOneField(NormalUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
	tagline = models.CharField(verbose_name="тэги", max_length=128, blank=True)
	about_me = models.TextField(verbose_name="о себе", blank=True)
	gender = models.CharField(verbose_name="пол", choices=GENDER_CHOICES, blank=True, max_length=5)

	lang = models.CharField(verbose_name="язык", blank=True, max_length=300)
	vk_link = models.CharField(verbose_name="ссылка вк", blank=True, max_length=300)

	@receiver(post_save, sender=NormalUser)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			UserProfile.objects.create(user=instance)


	@receiver(post_save, sender=NormalUser)
	def save_user_profile(sender, instance, **kwargs):
		instance.userprofile.save()