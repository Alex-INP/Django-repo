from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from users.models import NormalUser
from .forms import UserRegisterForm_Admin, UserUpdateForm_Admin, ProductCategoryForm_Admin, ProductForm_Admin
from products.models import ProductCategory, Product

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

@user_passes_test(lambda u: u.is_staff)
def admin_category_show(request):
	all_categories = ProductCategory.objects.all()
	categories_count = [len(Product.objects.filter(category=i.id)) for i in all_categories]
	context = {"title": "Категории",
			   "categories_data": list(zip(all_categories, categories_count))}
	return render(request, "admins/admin-category-show.html", context)

@user_passes_test(lambda u: u.is_staff)
def admin_category_create(request):
	context = {"title": "Создание категории"}
	if request.method == "POST":
		form = ProductCategoryForm_Admin(data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("admins:admin_category_show"))
	else:
		form = ProductCategoryForm_Admin()
		context["form"] = form
		return render(request, "admins/admin-category-create.html", context)


@user_passes_test(lambda u: u.is_staff)
def admin_category_update(request, id):
	context = {"title": "Редактирование категории"}
	current_category = ProductCategory.objects.get(id=id)
	if request.method == "POST":
		form = ProductCategoryForm_Admin(data=request.POST, instance=current_category)
		form.save()
		return HttpResponseRedirect(reverse("admins:admin_category_show"))
	else:
		context["form"] = ProductCategoryForm_Admin(instance=current_category)
		context["category"] = current_category
		return render(request, "admins/admin-category-update-delete.html", context)

@user_passes_test(lambda u: u.is_staff)
def admin_category_delete(request, id):
	current_category = ProductCategory.objects.get(id=id)
	current_category.delete()
	return HttpResponseRedirect(reverse("admins:admin_category_show"))

# -------------

@user_passes_test(lambda u: u.is_staff)
def admin_product_show(request):
	all_products = Product.objects.all()
	context = {"title": "Продукты",
			   "products_data": all_products}
	return render(request, "admins/admin-products-show.html", context)

@user_passes_test(lambda u: u.is_staff)
def admin_product_create(request):
	context = {"title": "Создание продукта"}
	if request.method == "POST":
		form = ProductForm_Admin(data=request.POST, files=request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("admins:admin_product_show"))
	else:
		form = ProductForm_Admin()
	context["form"] = form
	return render(request, "admins/admin-products-create.html", context)


@user_passes_test(lambda u: u.is_staff)
def admin_product_update(request, id):
	context = {"title": "Редактирование категории"}
	current_product = Product.objects.get(id=id)
	if request.method == "POST":
		form = ProductForm_Admin(data=request.POST, files=request.FILES, instance=current_product)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("admins:admin_product_show"))
	else:
		form = ProductForm_Admin(instance=current_product)
	context["form"] = form
	context["product"] = current_product
	return render(request, "admins/admin-products-update-delete.html", context)

@user_passes_test(lambda u: u.is_staff)
def admin_product_delete(request, id):
	current_product = Product.objects.get(id=id)
	current_product.delete()
	return HttpResponseRedirect(reverse("admins:admin_product_show"))