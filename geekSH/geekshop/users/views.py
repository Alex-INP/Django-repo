from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import View

from .forms import UserLoginForm, CreationForm, UserProfileForm, UserProfileEditForm
from .models import NormalUser
from geekshop import settings



# Create your views here.

class LoginView(View):
	template_name = "users/login.html"

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		login_form = UserLoginForm(data=self.request.POST)
		if login_form.is_valid():
			user = auth.authenticate(username=self.request.POST["username"], password=self.request.POST["password"])
			if user and user.is_active:
				auth.login(self.request, user)
				return HttpResponseRedirect(reverse("products:index"))
		return render(request, "users/login.html", self.get_context_data())

	def get_context_data(self, *, object_list=None, **kwargs):
		context = {}
		context["title"] = "GeekShop - Авторизация"
		context["form"] = UserLoginForm()
		return context

class RegisterView(CreateView):
	model = NormalUser
	form_class = CreationForm
	template_name = "users/register.html"
	success_url = reverse_lazy("users:login")

	def post(self, request, *args, **kwargs):
		creation_form = self.form_class(data=request.POST)
		if creation_form.is_valid():
			user = creation_form.save()
			if send_verify_link(user):
				messages.success(request, "Регистрация прошла успешно.")
			return HttpResponseRedirect(self.success_url)

		return render(request, "users/register.html", self.get_context_data())

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(RegisterView, self).get_context_data(**kwargs)
		context["title"] = "GeekShop - Регистрация"
		return context


class ProfileView(UpdateView):
	model = NormalUser
	form_class = UserProfileForm
	template_name = "users/profile.html"
	success_url = reverse_lazy("users:profile")

	def get(self, request, *args, **kwargs):
		self.object = self.model.objects.get(pk=request.user.pk)
		context = self.get_context_data(**kwargs)
		second_profile_form = UserProfileEditForm(instance=request.user.userprofile)
		context["second_form"] = second_profile_form
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		profile_form = self.form_class(data=request.POST, files=request.FILES, instance=request.user)
		second_profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
		if profile_form.is_valid() and second_profile_form.is_valid():
			profile_form.save()
			messages.success(request, "Изменения внесены")
			return HttpResponseRedirect(reverse('users:profile'))

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)
		context["title"] = "GeekShop - профиль"
		return context

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(ProfileView, self).dispatch(request, *args, **kwargs)


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse("index"))

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

# ---------------------------------------Old FBV---------------------------------------

# def login(request):
# 	context = {"title": "GeekShop - Авторизация"}
#
# 	if request.method == "POST":
# 		login_form = UserLoginForm(data=request.POST)
# 		if login_form.is_valid():
# 			user = auth.authenticate(username=request.POST["username"], password=request.POST["password"])
# 			if user and user.is_active:
# 				auth.login(request, user)
# 				return HttpResponseRedirect(reverse("products:index"))
# 	else:
# 		login_form = UserLoginForm()
# 	context["form"] = login_form
# 	return render(request, "users/login.html", context)

# def register(request):
# 	context = {"title": "GeekShop - Регистрация"}
# 	if request.method == "POST":
# 		creation_form = CreationForm(data=request.POST)
# 		if creation_form.is_valid():
# 			user = creation_form.save()
# 			if send_verify_link(user):
# 				messages.success(request, "Регистрация прошла успешно.")
# 			return HttpResponseRedirect(reverse("users:login"))
# 	else:
# 		creation_form = CreationForm()
# 	context["form"] = creation_form
# 	return render(request, "users/register.html", context)


# @login_required
# def profile(request):
# 	context = {"title": "GeekShop - профиль"}
# 	if request.method == "POST":
# 		profile_form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
# 		second_profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
# 		if profile_form.is_valid() and second_profile_form.is_valid():
# 			profile_form.save()
# 			messages.success(request, "Изменения внесены")
# 			return HttpResponseRedirect(reverse('users:profile'))
# 	else:
# 		profile_form = UserProfileForm(instance=request.user)
# 		second_profile_form = UserProfileEditForm(instance=request.user.userprofile)
# 		# context["baskets"] = Basket.objects.filter(user=request.user)
# 	context["form"] = profile_form
# 	context["second_form"] = second_profile_form
# 	return render(request, "users/profile.html", context)




