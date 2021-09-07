from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from .forms import UserLoginForm, CreationForm, UserProfileForm
from baskets.models import Basket

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
			creation_form.save()
			messages.success(request, "Регистрация прошла успешно.")
			return HttpResponseRedirect(reverse("users:login"))
	else:
		creation_form = CreationForm()
	context["form"] = creation_form
	return render(request, "users/register.html", context)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse("index"))

def profile(request):
	context = {"title": "GeekShop - профиль"}
	if request.method == "POST":
		profile_form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
		if profile_form.is_valid():
			profile_form.save()
			return HttpResponseRedirect(reverse('users:profile'))
	else:
		profile_form = UserProfileForm(instance=request.user)
		context["baskets"] = Basket.objects.filter(user=request.user)
	context["form"] = profile_form
	return render(request, "users/profile.html", context)
