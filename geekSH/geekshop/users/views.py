from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from .forms import UserLoginForm, CreationForm
# Create your views here.

def login(request):
	context = {"title": "GeekShop - Авторизация"}

	if request.method == "POST":
		login_form = UserLoginForm(data=request.POST)
		if login_form.is_valid():
			user = auth.authenticate(username=request.POST["username"], password=request.POST["password"])
			if user and user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect(reverse("index"))
		else:
			print(login_form.errors)
	else:
		login_form = UserLoginForm()
		context["form"] = login_form
		return render(request, "users/login.html", context)

def register(request):
	if request.method == "POST":
		creation_form = CreationForm(data=request.POST)
		if creation_form.is_valid():
			creation_form.save()
			return HttpResponseRedirect(reverse("index"))
		else:
			print(creation_form.errors)
	else:
		form = CreationForm
		context = {"title": "GeekShop - Регистрация", "form": form}
		return render(request, "users/register.html", context)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse("index"))
