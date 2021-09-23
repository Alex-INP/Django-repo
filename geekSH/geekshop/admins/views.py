from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from users.models import NormalUser
from .forms import UserRegisterForm_Admin, UserUpdateForm_Admin, ProductCategoryForm_Admin, ProductForm_Admin
from products.models import ProductCategory, Product

# Create your views here.

from django.http import JsonResponse
from django.template.loader import render_to_string

@user_passes_test(lambda u: u.is_staff)
def index(request):
	# print("ADMIN INDEX")
	return render(request, "admins/admin.html")

class UserListView(ListView):
	model = NormalUser
	context_object_name = "users"
	template_name = "admins/admin-users-read.html"

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object_list = self.get_queryset()
			context = self.get_context_data()
			result = render_to_string("admins/show.html", context)
			return JsonResponse({"result": result})


	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(UserListView, self).get_context_data(**kwargs)
		context["title"] = "Администрация"
		context["inbody_title"] = "Пользователи"
		context["table_titles"] = ["Имя пользователя", "Имя", "Фамилия", "Адрес эл. почты", "Персонал сайта", "Активный"]
		return context

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
	model = NormalUser
	form_class = UserRegisterForm_Admin
	context_object_name = "users"
	template_name = "admins/admin-users-create.html"
	success_url = reverse_lazy("admins:admin_users")

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = NormalUser()
			context = self.get_context_data()
			result = render_to_string("admins/create-update-user.html", context, request=request)
			return JsonResponse({"result": result})

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = None
			context = self.get_context_data()
			print(f"{request.POST=}")
			form = self.form_class(data=request.POST, files=request.FILES)
			if form.is_valid():
				form.save()
			result = render_to_string("admins/show.html", context, request=request)
			return JsonResponse({"result": result})

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(UserCreateView, self).get_context_data(**kwargs)
		context["title"] = "GeekShop - создание пользователя"
		context["inbody_title"] = "Создание пользователя"
		return context

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
	model = NormalUser
	form_class = UserUpdateForm_Admin
	context_object_name = "user"
	template_name = "admins/admin-users-update-delete.html"
	success_url = reverse_lazy("admins:admin_users")

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = NormalUser.objects.get(id=self.request.GET['pk'])
			context = self.get_context_data()
			result = render_to_string("admins/create-update-user.html", context, request=request)
			return JsonResponse({"result": result})

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = NormalUser.objects.get(id=self.request.POST['pk'])
			print(f"{self.object=}")
			context = self.get_context_data()
			form = self.form_class(data=request.POST, files=request.FILES, instance=self.object)
			if form.is_valid():
				form.save()
			result = render_to_string("admins/show.html", context, request=request)
			return JsonResponse({"result": result})
		else:
			print("NOT AJAX")

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(UserUpdateView, self).get_context_data(**kwargs)
		context["title"] = "GeekShop - редактирование пользователя"
		context["inbody_title"] = "Редактирование пользователя"
		return context

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
	model = NormalUser
	template_name = "admins/admin-users-update-delete.html"
	success_url = reverse_lazy("admins:admin_users")

	def delete(self, request, pk, **kwargs):
		print("Delete")
		self.object = NormalUser.objects.get(id=pk)
		self.object.is_active = False
		self.object.delete()
		return render(request, "admins/admin.html")

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

# ---------------------------------------Product Category CBV---------------------------------------

class CategoryListView(ListView):
	model = ProductCategory
	context_object_name = "categories_data"
	template_name = "admins/admin-category-show.html"

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object_list = self.get_queryset()
			context = self.get_context_data()
			result = render_to_string("admins/show.html", context)
			return JsonResponse({"result": result})

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(CategoryListView, self).get_context_data(**kwargs)
		context["title"] = "Категории"
		context["categories_data"] = list(zip(context["object_list"], [len(Product.objects.filter(category=i.pk)) for i in context["object_list"]]))
		context["inbody_title"] = "Категории товаров"
		context["table_titles"] = ["Имя категории", "Описание", "Количество продуктов в категории"]
		return context

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(CategoryListView, self).dispatch(request, *args, **kwargs)


class CategoryCreateView(CreateView):
	model = ProductCategory
	form_class = ProductCategoryForm_Admin
	template_name = "admins/admin-category-create.html"
	success_url = reverse_lazy("admins:admin_category_show")

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(CategoryCreateView, self).get_context_data(**kwargs)
		context["title"] = "Создание категории"
		return context

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(CategoryCreateView, self).dispatch(request, *args, **kwargs)

class CategoryUpdateView(UpdateView):
	model = ProductCategory
	context_object_name = "category"
	form_class = ProductCategoryForm_Admin
	template_name = "admins/admin-category-update-delete.html"
	success_url = reverse_lazy("admins:admin_category_show")

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(CategoryUpdateView, self).get_context_data(**kwargs)
		context["title"] = "Редактирование категории"
		return context

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)


class CategoryDeleteView(DeleteView):
	model = ProductCategory
	context_object_name = "category"
	template_name = "admins/admin-category-update-delete.html"
	success_url = reverse_lazy("admins:admin_category_show")

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(CategoryDeleteView, self).dispatch(request, *args, **kwargs)

# ---------------------------------------Products CBV---------------------------------------

class ProductListView(ListView):
	model = Product
	context_object_name = "products_data"
	template_name = "admins/admin-products-show.html"

	def get(self, request, *args, **kwargs):
		if request.is_ajax():

			self.object_list = self.get_queryset()
			context = self.get_context_data()
			result = render_to_string("admins/show.html", context)
			return JsonResponse({"result": result})

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(ProductListView, self).get_context_data(**kwargs)
		context["title"] = "Продукты"
		context["inbody_title"] = "Продукты"
		context["table_titles"] = ["Наименование", "Описание", "Цена", "Количество", "Изображение",
								   "Категория"]
		return context

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(ProductListView, self).dispatch(request, *args, **kwargs)

class ProductCreateView(CreateView):
	model = Product
	form_class = ProductForm_Admin
	context_object_name = "products_data"
	template_name = "admins/admin-products-create.html"
	success_url = reverse_lazy("admins:admin_product_show")

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(ProductCreateView, self).get_context_data(**kwargs)
		context["title"] = "Создание продукта"
		return context

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(ProductCreateView, self).dispatch(request, *args, **kwargs)


class ProductUpdateView(UpdateView):
	model = Product
	context_object_name = "product"
	form_class = ProductForm_Admin
	template_name = "admins/admin-products-update-delete.html"
	success_url = reverse_lazy("admins:admin_product_show")

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(ProductUpdateView, self).get_context_data(**kwargs)
		context["title"] = "Редактирование продукта"
		return context

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(ProductUpdateView, self).dispatch(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
	model = Product
	context_object_name = "product"
	template_name = "admins/admin-product-update-delete.html"
	success_url = reverse_lazy("admins:admin_product_show")

	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(ProductDeleteView, self).dispatch(request, *args, **kwargs)

# ---------------------------------------Old FBV---------------------------------------

# @user_passes_test(lambda u: u.is_staff)
# def admin_users(request):
# 	context = {"users": NormalUser.objects.all()}
# 	return render(request, "admins/admin-users-read.html", context)

# @user_passes_test(lambda u: u.is_staff)
# def admin_users_create(request):
# 	context = {"title": "GeekShop - создание пользователя"}
#
# 	if request.method == "POST":
# 		creation_form = UserRegisterForm_Admin(data=request.POST, files=request.FILES)
# 		if creation_form.is_valid():
# 			creation_form.save()
# 			return HttpResponseRedirect(reverse("admins:admin_users"))
# 	else:
# 		creation_form = UserRegisterForm_Admin()
# 	context["form"] = creation_form
# 	return render(request, "admins/admin-users-create.html", context)

# @user_passes_test(lambda u: u.is_staff)
# def admin_users_update(request, id):
# 	context = {"title": "GeekShop - редактирование пользователя"}
# 	current_user = NormalUser.objects.get(id=id)
# 	if request.method == "POST":
# 		profile_form = UserUpdateForm_Admin(data=request.POST, files=request.FILES, instance=current_user)
# 		if profile_form.is_valid():
# 			profile_form.save()
# 			return HttpResponseRedirect(reverse('admins:admin_users'))
# 	else:
# 		profile_form = UserUpdateForm_Admin(instance=current_user)
# 	context["user"] = current_user
# 	context["form"] = profile_form
#
# 	return render(request, "admins/admin-users-update-delete.html", context)

# @user_passes_test(lambda u: u.is_staff)
# def admin_users_delete(request, id):
# 	user_to_delete = NormalUser.objects.get(id=id)
# 	user_to_delete.is_active = False
# 	user_to_delete.save()
# 	return HttpResponseRedirect(reverse('admins:admin_users'))

# @user_passes_test(lambda u: u.is_staff)
# def admin_category_show(request):
# 	all_categories = ProductCategory.objects.all()
# 	categories_count = [len(Product.objects.filter(category=i.id)) for i in all_categories]
# 	context = {"title": "Категории",
# 			   "categories_data": list(zip(all_categories, categories_count))}
# 	return render(request, "admins/admin-category-show.html", context)

# @user_passes_test(lambda u: u.is_staff)
# def admin_category_create(request):
# 	context = {"title": "Создание категории"}
# 	if request.method == "POST":
# 		form = ProductCategoryForm_Admin(data=request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect(reverse("admins:admin_category_show"))
# 	else:
# 		form = ProductCategoryForm_Admin()
# 		context["form"] = form
# 		return render(request, "admins/admin-category-create.html", context)

# @user_passes_test(lambda u: u.is_staff)
# def admin_category_update(request, id):
# 	context = {"title": "Редактирование категории"}
# 	current_category = ProductCategory.objects.get(id=id)
# 	if request.method == "POST":
# 		form = ProductCategoryForm_Admin(data=request.POST, instance=current_category)
# 		form.save()
# 		return HttpResponseRedirect(reverse("admins:admin_category_show"))
# 	else:
# 		context["form"] = ProductCategoryForm_Admin(instance=current_category)
# 		context["category"] = current_category
# 		return render(request, "admins/admin-category-update-delete.html", context)

# @user_passes_test(lambda u: u.is_staff)
# def admin_category_delete(request, id):
# 	current_category = ProductCategory.objects.get(id=id)
# 	current_category.delete()
# 	return HttpResponseRedirect(reverse("admins:admin_category_show"))

# -------------

# @user_passes_test(lambda u: u.is_staff)
# def admin_product_show(request):
# 	all_products = Product.objects.all()
# 	context = {"title": "Продукты",
# 			   "products_data": all_products}
# 	return render(request, "admins/admin-products-show.html", context)

# @user_passes_test(lambda u: u.is_staff)
# def admin_product_create(request):
# 	context = {"title": "Создание продукта"}
# 	if request.method == "POST":
# 		form = ProductForm_Admin(data=request.POST, files=request.FILES)
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect(reverse("admins:admin_product_show"))
# 	else:
# 		form = ProductForm_Admin()
# 	context["form"] = form
# 	return render(request, "admins/admin-products-create.html", context)


# @user_passes_test(lambda u: u.is_staff)
# def admin_product_update(request, id):
# 	context = {"title": "Редактирование категории"}
# 	current_product = Product.objects.get(id=id)
# 	if request.method == "POST":
# 		form = ProductForm_Admin(data=request.POST, files=request.FILES, instance=current_product)
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect(reverse("admins:admin_product_show"))
# 	else:
# 		form = ProductForm_Admin(instance=current_product)
# 	context["form"] = form
# 	context["product"] = current_product
# 	return render(request, "admins/admin-products-update-delete.html", context)
#
# @user_passes_test(lambda u: u.is_staff)
# def admin_product_delete(request, id):
# 	current_product = Product.objects.get(id=id)
# 	current_product.delete()
# 	return HttpResponseRedirect(reverse("admins:admin_product_show"))