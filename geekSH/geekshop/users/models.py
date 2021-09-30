from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta
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