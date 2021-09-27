import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from .models import NormalUser
from .validators import validate_password

class UserProfileForm(UserChangeForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4", "readonly": True}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control py-4", "readonly": True}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4", "placeholder": "Введите имя"}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4", "placeholder": "Введите фамилию"}))
	image = forms.ImageField(widget=forms.FileInput(attrs={"class": "custom-file-input"}), required=False)

	class Meta:
		model = NormalUser
		fields = ("username", "email", "first_name", "last_name", "image", "age")

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4",
															  "placeholder": "Введите имя пользователя"}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control py-4",
															 "placeholder": "Введите пароль"}))
	class Meta:
		model = NormalUser
		fields = ("username", "password")

class CreationForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput())
	email = forms.CharField(widget=forms.EmailInput())
	first_name = forms.CharField(widget=forms.TextInput())
	last_name = forms.CharField(widget=forms.TextInput())
	age = forms.IntegerField(widget=forms.NumberInput(), required=False)
	password1 = forms.CharField(widget=forms.PasswordInput()) # , validators=[validate_password])
	password2 = forms.CharField(widget=forms.PasswordInput()) #, validators=[validate_password])

	class Meta:
		model = NormalUser
		fields = ("username", "email", "first_name", "last_name", "password1", "password2")

	def __init__(self, *args, **kwargs):
		super(CreationForm, self).__init__(*args, **kwargs)
		self.fields["username"].widget.attrs["placeholder"] = "Введите имя пользователя"
		self.fields["email"].widget.attrs["placeholder"] = "Введите почту"
		self.fields["first_name"].widget.attrs["placeholder"] = "Введите имя"
		self.fields["last_name"].widget.attrs["placeholder"] = "Введите фамилию"
		self.fields["age"].widget.attrs["placeholder"] = "Введите возраст"
		self.fields["password1"].widget.attrs["placeholder"] = "Введите пароль"
		self.fields["password2"].widget.attrs["placeholder"] = "Повторите пароль"
		for name, field in self.fields.items():
			field.widget.attrs["class"] = "form-control py-4"
	
	def save(self, commit=True):
		user = super(CreationForm, self).save()
		user.is_active = False
		salt = hashlib.sha1(str(random.random()).encode("utf8")).hexdigest()[:6]
		user.activation_key = hashlib.sha1((user.email + salt).encode("utf8")).hexdigest()
		user.save()
		return user