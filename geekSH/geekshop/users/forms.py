from django.contrib.auth.forms import AuthenticationForm

from .models import NormalUser

class UserLoginForm(AuthenticationForm):
	class Meta:
		model = NormalUser
		fields = ("username", "password")
