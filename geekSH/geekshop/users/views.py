from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .forms import UserLoginForm, CreationForm, UserProfileForm
from baskets.models import Basket
from .models import NormalUser
from geekshop import settings

# Create your views here.

def login(request):
	context = {"title": "GeekShop - Авторизация"}

	if request.method == "POST":
		login_form = UserLoginForm(data=request.POST)
		if login_form.is_valid():
			user = auth.authenticate(username=request.POST["username"], password=request.POST["password"])
			if user and user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect(reverse("products:index"))
	else:
		login_form = UserLoginForm()
	context["form"] = login_form
	return render(request, "users/login.html", context)

def register(request):
	context = {"title": "GeekShop - Регистрация"}
	if request.method == "POST":
		creation_form = CreationForm(data=request.POST)
		if creation_form.is_valid():
			user = creation_form.save()
			if send_verify_link(user):
				messages.success(request, "Регистрация прошла успешно.")
			return HttpResponseRedirect(reverse("users:login"))
	else:
		creation_form = CreationForm()
	context["form"] = creation_form
	return render(request, "users/register.html", context)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse("index"))

@login_required
def profile(request):
	context = {"title": "GeekShop - профиль"}
	if request.method == "POST":
		profile_form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
		if profile_form.is_valid():
			profile_form.save()
			messages.success(request, "Изменения внесены")
			return HttpResponseRedirect(reverse('users:profile'))
	else:
		profile_form = UserProfileForm(instance=request.user)
		# context["baskets"] = Basket.objects.filter(user=request.user)
	context["form"] = profile_form
	return render(request, "users/profile.html", context)

def send_verify_link(user):
	verify_link = reverse("users:verify", args=[user.email, user.activation_key])
	subject = f"Для активации учетной записи {user.username}, пройдите по ссылке"
	message = f"Ссылка для подтверждения учетной записи {user.username} на портале:\n{settings.DOMAIN_NAME}{verify_link}"
	return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def verify(request, email, activation_key):
	try:
		user = NormalUser.objects.get(email=email)
		if user and user.activation_key == activation_key and not user.is_activation_key_expired():
			user.activation_key = ""
			user.activation_key_expires = None
			user.is_active = True
			user.save()
			auth.login(request, user)
		return render(request, "users/verification.html")
	except:
		return HttpResponseRedirect(reverse("index"))


