from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from users.models import NormalUser
from .forms import UserRegisterForm_Admin, UserUpdateForm_Admin

# Create your views here.

@user_passes_test(lambda u: u.is_staff)
def index(request):
	return render(request, "admins/admin.html")

@user_passes_test(lambda u: u.is_staff)
def admin_users(request):
	context = {"users": NormalUser.objects.all()}
	return render(request, "admins/admin-users-read.html", context)

@user_passes_test(lambda u: u.is_staff)
def admin_users_create(request):
	context = {"title": "GeekShop - создание пользователя"}

	if request.method == "POST":
		creation_form = UserRegisterForm_Admin(data=request.POST, files=request.FILES)
		if creation_form.is_valid():
			creation_form.save()
			return HttpResponseRedirect(reverse("admins:admin_users"))
	else:
		creation_form = UserRegisterForm_Admin()
	context["form"] = creation_form
	return render(request, "admins/admin-users-create.html", context)

@user_passes_test(lambda u: u.is_staff)
def admin_users_update(request, id):
	context = {"title": "GeekShop - редактирование пользователя"}
	current_user = NormalUser.objects.get(id=id)
	if request.method == "POST":
		profile_form = UserUpdateForm_Admin(data=request.POST, files=request.FILES, instance=current_user)
		if profile_form.is_valid():
			profile_form.save()
			return HttpResponseRedirect(reverse('admins:admin_users'))
	else:
		profile_form = UserUpdateForm_Admin(instance=current_user)
	context["user"] = current_user
	context["form"] = profile_form

	return render(request, "admins/admin-users-update-delete.html", context)

@user_passes_test(lambda u: u.is_staff)
def admin_users_delete(request, id):
	user_to_delete = NormalUser.objects.get(id=id)
	user_to_delete.is_active = False
	user_to_delete.save()
	return HttpResponseRedirect(reverse('admins:admin_users'))
