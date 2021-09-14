from django import forms

from users.forms import CreationForm, UserProfileForm
from users.models import NormalUser

class UserRegisterForm_Admin(CreationForm):
	image = forms.ImageField(widget=forms.FileInput(), required=False)

	class Meta:
		model = NormalUser
		fields = ("username", "email", "image", "first_name", "last_name", "password1", "password2")

class UserUpdateForm_Admin(UserProfileForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4", "readonly": False}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control py-4", "readonly": False}))

	class Meta:
		model = NormalUser
		fields = ("username", "email", "first_name", "last_name", "image")
