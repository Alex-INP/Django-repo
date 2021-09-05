from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from .models import NormalUser
from .validators import validate_password

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4",
															  "placeholder": "Введите имя пользователя"}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control py-4",
															 "placeholder": "Введите пароль"}))
	class Meta:
		model = NormalUser
		fields = ("username", "password")

class CreationForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4",
															 "placeholder": "Введите имя пользователя"}))
	email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control py-4",
															 "placeholder": "Введите почту"}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4",
															 "placeholder": "Введите имя"}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4",
															 "placeholder": "Введите фамилию"}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control py-4",
															 "placeholder": "Введите пароль"}), validators=[validate_password])
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control py-4",
															 "placeholder": "Повторите пароль"}), validators=[validate_password])
	class Meta:
		model = NormalUser
		fields = ("username", "email", "first_name", "last_name", "password1", "password2")
